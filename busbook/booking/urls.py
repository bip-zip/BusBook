from django.conf.urls import url
from .views import *
from django.urls import path,include
from .views import *


app_name='booking'

urlpatterns=[
    path('', HomeView.as_view(), name='home'),
    path('results', ResultView.as_view(), name='result'),
    path('route/<int:id>', RouteDetail.as_view(), name='route'),
    path('your-bookings', BookingList.as_view(), name='bookinglist'),

]