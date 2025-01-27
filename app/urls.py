from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from.views import(BasePageView, AdminPageView, HomePageView, ContactPageView, AboutPageView, ServicesPageView,
                  AdminCreateView, UserCreateView, AppointmentCreateView, ServiceCreateView, TherapistCreateView,
                  AvailabilityCreateView, ServiceListView, ServiceDetailView,
                  AdminDeleteView, UserDeleteView, AppointmentDeleteView, ServiceDeleteView, TherapistDeleteView,
                  AvailabilityDeleteView,
                  AdminUpdateView, UserUpdateView, AppointmentUpdateView, ServiceUpdateView, TherapistUpdateView,
                  AvailabilityUpdateView, account_settings, RescheduleUpdateView, CustomerSchedDeleteView,)

urlpatterns = [
    path('', BasePageView.as_view(), name='base'),
    path('home/', HomePageView.as_view(), name='home'),
    path('serviceview/', ServiceListView.as_view(), name='service_view'),
    path('detail_view/<int:pk>', ServiceDetailView.as_view(), name='detail_view'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('service/', ServicesPageView.as_view(), name='service'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('account/', account_settings, name='account'),
    path('database/', AdminPageView.as_view(), name='database'),
    path('booking/', views.BookingPageView.as_view(), name='booking_page'),
    path('reschedule/<int:pk>/', RescheduleUpdateView.as_view(), name='reschedule_page'),
    path('appointment/<int:pk>/delete/', CustomerSchedDeleteView.as_view(), name='customer_schedule_delete'),

    path('login/', views.customer_login, name='customer_login'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('register/', views.register_customer, name='register_customer'),

    path('dbadmin/create', AdminCreateView.as_view(), name='create_admin'),
    path('dbuser/create', UserCreateView.as_view(), name='create_user'),
    path('create-appointment/', AppointmentCreateView.as_view(), name='create_appointment'),
    path('dbservice/create', ServiceCreateView.as_view(), name='create_service'),
    path('dbtherapist/create', TherapistCreateView.as_view(), name='create_therapist'),
    path('dbavailability/create', AvailabilityCreateView.as_view(), name='create_availability'),

    path('update_admin/<int:pk>/', AdminUpdateView.as_view(), name='update_admin'),
    path('update_user/<int:pk>/', UserUpdateView.as_view(), name='update_user'),
    path('update_appointment/<int:pk>/', AppointmentUpdateView.as_view(), name='update_appointment'),
    path('update_service/<int:pk>/', ServiceUpdateView.as_view(), name='update_service'),
    path('update_therapist/update/<int:pk>/', TherapistUpdateView.as_view(), name='update_therapist'),
    path('update_availability/<int:pk>/update/', AvailabilityUpdateView.as_view(), name='update_availability'),

    path('dbadmin/<int:pk>/delete', AdminDeleteView.as_view(), name='admin_delete'),
    path('dbuser/<int:pk>/delete', UserDeleteView.as_view(), name='user_delete'),
    path('dbappointment/<int:pk>/delete', AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('dbservice/<int:pk>/delete', ServiceDeleteView.as_view(), name='service_delete'),
    path('dbtherapist/<int:pk>/delete', TherapistDeleteView.as_view(), name='therapist_delete'),
    path('dbavailability/<int:pk>/delete', AvailabilityDeleteView.as_view(), name='availability_delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)