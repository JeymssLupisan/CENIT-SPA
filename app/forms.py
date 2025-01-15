from django import forms
from .models import Appointment, Customer, Therapist, Service, Availability
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ValidationError


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['customer', 'therapist', 'service', 'date', 'status']
        widgets = {
            'date': forms.TextInput(attrs={
                'class': 'flatpickr form-control',
                'placeholder': 'Select Date and Time',
            }),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        therapist = self.cleaned_data['therapist']

        if not Availability.objects.filter(therapist=therapist, date=date.date()).exists():
            raise ValidationError("The therapist is not available on the selected date.")

        if date.time() < therapist.working_hours_start or date.time() > therapist.working_hours_end:
            raise ValidationError("Selected time is outside the therapist's working hours.")

        if Appointment.objects.filter(therapist=therapist, date=date).exists():
            raise ValidationError("The selected time slot is already booked.")

        return date


class RescheduleForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'therapist', 'date']

    def clean_date(self):
        date = self.cleaned_data['date']
        therapist = self.cleaned_data['therapist']

        if not Availability.objects.filter(therapist=therapist, date=date.date()).exists():
            raise ValidationError("The therapist is not available on the selected date.")

        if date.time() < therapist.working_hours_start or date.time() > therapist.working_hours_end:
            raise ValidationError("Selected time is outside the therapist's working hours.")

        if Appointment.objects.filter(therapist=therapist, date=date).exists():
            raise ValidationError("The selected time slot is already booked.")

        return date


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'duration', 'price', 'image']
        widgets = {
            'duration': forms.TextInput(attrs={'type': 'number', 'step': '1'}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['therapist', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now().date():
            raise forms.ValidationError("The selected date cannot be in the past.")
        return date


class TherapistForm(forms.ModelForm):
    class Meta:
        model = Therapist
        fields = ['name', 'max_daily_appointments', 'working_hours_start', 'working_hours_end', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Therapist Name'}),
            'max_daily_appointments': forms.NumberInput(attrs={'placeholder': 'Max Daily Appointments'}),
            'working_hours_start': forms.TimeInput(attrs={'type': 'time'}),
            'working_hours_end': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'placeholder': 'Therapist Description', 'rows': 5}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("working_hours_start")
        end_time = cleaned_data.get("working_hours_end")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("Working hours start time must be earlier than the end time.")

        return cleaned_data


class AvailabilityForm2(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['therapist', 'date']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now().date():
            raise forms.ValidationError("The selected date cannot be in the past.")
        return date


class CustomerAppointmentForm(forms.ModelForm):
    therapist = forms.ModelChoiceField(queryset=Therapist.objects.all(), empty_label="Select Therapist")
    service = forms.ModelChoiceField(queryset=Service.objects.all(), empty_label="Select Service")

    class Meta:
        model = Appointment
        fields = ['therapist', 'service', 'date']

    def save(self, commit=True):
        appointment = super().save(commit=False)
        appointment.status = 'booked'
        if commit:
            appointment.save()
        return appointment
