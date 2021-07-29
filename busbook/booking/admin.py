from django.contrib import admin
from .models import *

admin.site.register(Bus)
admin.site.register(BusCompany)
admin.site.register(Seat)




@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):  # instead of ModelAdmin
    list_display=('source', 'destination', 'time','date','fare')
    list_display_links=('source','destination')
    search_fields=('source','destination')
    list_per_page =25

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):  # instead of ModelAdmin
    list_display=('route', 'user', 'seat','date_created','cancelled')
    list_display_links=('route',)
    search_fields=('cancelled',)
    list_per_page =25

# Register your models here.
