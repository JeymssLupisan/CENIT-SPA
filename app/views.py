from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.db import transaction
from django.http import JsonResponse
from .models import Admin, Customer, Appointment, Service, Therapist, Availability
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from .forms import (AppointmentForm, AvailabilityForm, ServiceForm, TherapistForm, AvailabilityForm2,
                    CustomerAppointmentForm, RescheduleForm)
from django.utils import timezone


class BasePageView(TemplateView):
    template_name = 'app/base.html'


class HomePageView(TemplateView):
    template_name = 'app/home.html'


class AboutPageView(TemplateView):
    template_name = 'app/about.html'


class ServicesPageView(TemplateView):
    template_name = 'app/services.html'


class ContactPageView(TemplateView):
    template_name = 'app/contact.html'


class BookingPageView(TemplateView):
    template_name = 'app/booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        therapists = Therapist.objects.all()
        available_therapists = []

        for therapist in therapists:
            availability = Availability.objects.filter(therapist=therapist, date=today).first()

            if availability:
                current_bookings = Appointment.objects.filter(
                    therapist=therapist,
                    date__date=today
                ).count()

                remaining_slots = therapist.max_daily_appointments - current_bookings

                if remaining_slots > 0:
                    available_therapists.append({
                        'therapist': therapist,
                        'current_bookings': current_bookings,
                        'remaining_slots': remaining_slots
                    })

        context['available_therapists'] = available_therapists
        context['form'] = CustomerAppointmentForm()
        return context

    def post(self, request, *args, **kwargs):
        if 'customer_id' not in request.session:
            messages.error(request, "You need to be logged in to book an appointment.")
            return redirect('base')

        form = CustomerAppointmentForm(request.POST)
        if form.is_valid():
            therapist = form.cleaned_data['therapist']
            date = form.cleaned_data['date']
            service = form.cleaned_data['service']

            if date.time() < therapist.working_hours_start or date.time() > therapist.working_hours_end:
                messages.error(request, f"Selected time is outside the therapist's working hours ({therapist.working_hours_start} - {therapist.working_hours_end}).")
                return self.get(request, *args, **kwargs)

            if date < timezone.now():
                messages.error(request, "You cannot book an appointment in the past.")
                return self.get(request, *args, **kwargs)

            availability = Availability.objects.filter(therapist=therapist, date=date).first()
            if not availability:
                messages.error(request, "The selected therapist is not available on this day.")
                return self.get(request, *args, **kwargs)

            current_bookings = Appointment.objects.filter(
                therapist=therapist,
                date__date=date
            ).count()

            remaining_slots = therapist.max_daily_appointments - current_bookings

            if remaining_slots <= 0:
                messages.error(request, "No available slots for this therapist on the selected day.")
                return self.get(request, *args, **kwargs)

            try:
                with transaction.atomic():
                    appointment = form.save(commit=False)
                    customer = Customer.objects.get(id=request.session['customer_id'])
                    appointment.customer = customer

                    appointment.save()

                    customer.loyalty_points += 2
                    customer.save()

                    messages.success(request, "Your appointment has been booked successfully! You've earned 2 loyalty points.")
                    return redirect('booking_page')

            except ValidationError as e:
                messages.error(request, f"Error: {str(e)}")
                return self.get(request, *args, **kwargs)

        else:
            messages.error(request, f"There was an error with your booking: {form.errors}")
            return self.get(request, *args, **kwargs)


class AdminPageView(TemplateView):
    template_name = 'app/admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admins'] = Admin.objects.all()
        context['users'] = Customer.objects.all()
        context['appointments'] = Appointment.objects.all()
        context['services'] = Service.objects.all()
        context['therapists'] = Therapist.objects.all()
        context['availabilities'] = Availability.objects.all()

        admin_firstname = self.request.session.get('admin_firstname')
        context['admin_firstname'] = admin_firstname
        return context


class AdminCreateView(CreateView):
    model = Admin
    fields = ['firstname', 'lastname', 'username', 'email', 'password']
    template_name = 'app/add_admin.html'

    def get_success_url(self):
        return reverse_lazy('database') + '?section=admins'


class UserCreateView(CreateView):
    model = Customer
    fields = ['name', 'username', 'email', 'password', 'loyalty_points']
    template_name = 'app/add_user.html'

    def get_success_url(self):
        return reverse_lazy('database') + '?section=users'


class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'app/add_appointment.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Appointment created successfully!")
        return response

    def get_success_url(self):
        return reverse_lazy('database') + '?section=appointments'

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your form submission.")
        return super().form_invalid(form)


class ServiceCreateView(CreateView):
    model = Service
    fields = ['name', 'description', 'duration', 'price', 'image']
    template_name = 'app/add_service.html'

    def get_success_url(self):
        return reverse_lazy('database') + '?section=services'


class TherapistCreateView(CreateView):
    model = Therapist
    fields = ['name', 'max_daily_appointments', 'working_hours_start', 'working_hours_end', 'description']
    template_name = 'app/add_therapist.html'

    def get_success_url(self):
        return reverse_lazy('database') + '?section=therapists'


class AvailabilityCreateView(CreateView):
    model = Availability
    form_class = AvailabilityForm
    template_name = 'app/add_availability.html'

    def get_success_url(self):
        return reverse_lazy('database') + '?section=availability'

    def form_valid(self, form):
        messages.success(self.request, "Availability added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error in adding availability.")
        return super().form_invalid(form)


class AdminUpdateView(UpdateView):
    model = Admin
    fields = ['firstname', 'lastname', 'username', 'email', 'password']
    template_name = 'app/update_admin.html'

    def get_success_url(self):
        return reverse_lazy('database') + '?section=admins'


class UserUpdateView(UpdateView):
    model = Customer
    fields = ['name', 'username', 'email', 'password', 'loyalty_points']
    template_name = 'app/update_user.html'

    def get_success_url(self):
        return reverse_lazy('database') + '?section=users'


class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'app/update_appointment.html'

    def get_success_url(self):
        return reverse_lazy('database') + '?section=appointments'

    def get_object(self, queryset=None):
        return get_object_or_404(Appointment, pk=self.kwargs['pk'])


class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'app/update_service.html'

    def get_success_url(self):
        return reverse_lazy('database') + '?section=services'

    def get_object(self, queryset=None):
        return get_object_or_404(Service, pk=self.kwargs['pk'])

    def form_valid(self, form):
        return super().form_valid(form)


class TherapistUpdateView(UpdateView):
    model = Therapist
    form_class = TherapistForm
    template_name = 'app/update_therapist.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Therapist, pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('database') + '?section=therapists'

    def form_valid(self, form):
        print("Form is valid:", form.cleaned_data)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid:", form.errors)
        return super().form_invalid(form)


class AvailabilityUpdateView(UpdateView):
    model = Availability
    form_class = AvailabilityForm
    template_name = 'app/update_availability.html'

    def get_success_url(self):
        return reverse_lazy('database') + '?section=availability'

    def get_object(self, queryset=None):
        return get_object_or_404(Availability, pk=self.kwargs['pk'])


class RescheduleUpdateView(UpdateView):
    model = Appointment
    form_class = RescheduleForm
    template_name = 'app/reschedule.html'

    def get_success_url(self):
        return reverse_lazy('account')

    def get_object(self, queryset=None):
        return get_object_or_404(Appointment, pk=self.kwargs['pk'])

    def form_valid(self, form):
        try:
            form.clean()
        except ValidationError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)

        return super().form_valid(form)



class AdminDeleteView(DeleteView):
    model = Admin
    template_name = 'app/delete_admin.html'

    def get_success_url(self):
        return reverse_lazy('database') + '?section=admins'


class UserDeleteView(DeleteView):
    model = Customer
    template_name = 'app/delete_user.html'

    def get_success_url(self):
        return reverse_lazy('database') + '?section=users'


class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'app/delete_service.html'

    def get_success_url(self):
        return reverse_lazy('database') + '?section=services'


class TherapistDeleteView(DeleteView):
    model = Therapist
    template_name = 'app/delete_therapist.html'

    def get_success_url(self):
        return reverse_lazy('database') + '?section=therapists'


class AppointmentDeleteView(DeleteView):
    model = Appointment
    template_name = 'app/delete_appointment.html'

    def get_success_url(self):
        return reverse_lazy('database') + '?section=appointments'


class AvailabilityDeleteView(DeleteView):
    model = Availability
    template_name = 'app/delete_availability.html'

    def get_success_url(self):
        return reverse_lazy('database') + '?section=availability'


class CustomerSchedDeleteView(DeleteView):
    model = Appointment
    template_name = 'app/account.html'

    def get_success_url(self):
        return reverse_lazy('account')


def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            customer = Customer.objects.get(username=username)
            if customer.password == password:
                request.session['customer_id'] = customer.id
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        except Customer.DoesNotExist:
            messages.error(request, "Customer does not exist. Please register first.")

    return render(request, 'app/base.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            admin = Admin.objects.get(username=username)
            if admin.password == password:
                request.session['admin_id'] = admin.id
                request.session['admin_firstname'] = admin.firstname
                messages.success(request, "Admin login successful.")
                return redirect('database')
            else:
                messages.error(request, "Invalid username or password.")
        except Admin.DoesNotExist:
            messages.error(request, "Admin does not exist. Please contact support.")

    return render(request, 'app/admin_login.html')


def register_customer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if Customer.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register_customer')

        customer = Customer(
            name=name,
            username=username,
            email=email,
            password=password,
        )
        customer.save()
        messages.success(request, "Registration successful!")
        return redirect('base')

    return render(request, 'app/base.html')


def account_settings(request):
    if 'customer_id' not in request.session:
        return redirect('base')

    customer_id = request.session['customer_id']
    try:
        customer = Customer.objects.get(id=customer_id)
    except User.DoesNotExist:
        raise Http404("User does not exist")

    appointments = Appointment.objects.filter(customer=customer)

    return render(request, 'app/account.html', {
        'customer': customer,
        'appointments': appointments
    })
