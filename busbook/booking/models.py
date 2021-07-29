from django.db import models
from bususer.models import User
from datetime import datetime


class BusCompany(models.Model):
    name= models.CharField(max_length=100)
    phone=models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Bus(models.Model):
    bus_no= models.CharField(max_length=50)
    company=models.ForeignKey(BusCompany, on_delete=models.CASCADE)
    totalseat=models.IntegerField(default=0)
    ac= models.BooleanField(default=False)
    driver= models.CharField(max_length=100)
    phone=models.CharField(max_length=15)
    photo=models.ImageField(upload_to='buspic')
    
    def __str__(self):
        return self.bus_no



class Route(models.Model):
    bus=models.ForeignKey(Bus, on_delete=models.CASCADE)
    source=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    date=models.DateField()
    time= models.CharField(max_length=5)
    fare=models.IntegerField(null=False)

    def __str__(self):
        return ((self.source).capitalize() + ' to ' + (self.destination).capitalize())

    @property
    def available_seats(self):
        seats=Reservation.objects.filter(route=self, cancelled=False).values_list('seat')
        av_seats= Seat.objects.exclude(seat_id__in=seats)
        return av_seats

    @property
    def available_seats_no(self):
        seats=Reservation.objects.filter(route=self, cancelled=False).values_list('seat')
        av_seats= Seat.objects.exclude(seat_id__in=seats).count()
        return av_seats


class Seat(models.Model):
    seat_id=models.CharField(max_length=10, primary_key=True)

    def __str__(self):
        return self.seat_id


class Reservation(models.Model):
    route=models.ForeignKey(Route, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    seat=models.ForeignKey(Seat, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    cancelled=models.BooleanField(default=False)
    user_phone=models.CharField(max_length=15, null=True)

    def __str__(self):
        return str(self.id)
