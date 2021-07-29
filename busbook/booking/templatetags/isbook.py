from django import template
from booking.models import *
register = template.Library()

@register.filter(name='isbooked')

def isbooked(route,seat):
    route=Route.objects.get(id=route)
    seat_obj=Seat.objects.get(seat_id=seat)
    reservation=Reservation.objects.filter(route=route, cancelled=False, seat=seat_obj).exists()

    if reservation:
        return True
    
    return False


