from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta


class Admin(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username


class Customer(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=150, unique=True, default="")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    loyalty_points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.DurationField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/service', null=True, blank=True)

    def __str__(self):
        return self.name


class Therapist(models.Model):
    name = models.CharField(max_length=100)
    max_daily_appointments = models.PositiveIntegerField(default=5)
    working_hours_start = models.TimeField(default='08:00:00')
    working_hours_end = models.TimeField(default='17:00:00')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def booked_slots(self, date):
        return Appointment.objects.filter(therapist=self, date__date=date).count()

    def is_available(self, date):
        return Availability.objects.filter(therapist=self, date=date).exists()


class Availability(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.therapist.name} available on {self.date}"

    def clean(self):
        if Availability.objects.filter(therapist=self.therapist, date=self.date).exists():
            raise ValidationError(f"The therapist {self.therapist.name} is already marked as available on {self.date}.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ]

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='booked')

    class Meta:
        unique_together = ('therapist', 'date')

    def save(self, *args, **kwargs):
        if not self.therapist.is_available(self.date.date()):
            raise ValidationError("The therapist is not available on the selected date.")
        if self.date.time() < self.therapist.working_hours_start or self.date.time() > self.therapist.working_hours_end:
            raise ValidationError("Selected time is outside the therapist's working hours.")
        if self.therapist.booked_slots(self.date.date()) >= self.therapist.max_daily_appointments:
            raise ValidationError("The therapist has reached the daily appointment limit.")
        if Appointment.objects.filter(therapist=self.therapist, date=self.date).exists():
            raise ValidationError("The selected time slot is already booked.")
        super().save(*args, **kwargs)

    def get_total_cost(self):
        return self.service.price

    def __str__(self):
        return self.customer.name
