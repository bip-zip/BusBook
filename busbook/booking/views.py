from django.shortcuts import render
from .models import Route,Seat, Reservation
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
# Create your views here.
from django.views.generic import TemplateView, View, ListView
from django.core.mail import send_mail

class HomeView(TemplateView):
    template_name='booking/index.html'


class ResultView(TemplateView):
    template_name='booking/results.html'

    def get(self,request):
        source=request.GET['source'].lower()
        destination=request.GET['destination'].lower()
        date=request.GET['date']

        route= Route.objects.filter(source=source, destination=destination, date=date)
        
        return render(request, self.template_name, {'route':route})


class RouteDetail(TemplateView):
    template_name='booking/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        routeid= self.kwargs['id']
        route=Route.objects.get(id=routeid)
        context.update({'route':route})
        return context

    @method_decorator(login_required)
    def post(self,*args,**kwargs):
        routeid= self.kwargs['id']
        route=Route.objects.get(id=routeid)
        user=self.request.user
        seatid=self.request.POST.get('seat_id')
        phone=self.request.POST.get('phone')

        seat=Seat.objects.get(seat_id=seatid)
        Reservation.objects.create(user=user, seat=seat, route=route, user_phone=phone)
        message=('Hello, Dear '+user.first_name + ' ' + user.last_name +' your bus for '+ str(route) +' on '+ str(route.date) + ',' + str(route.time) +' has been booked. Thank you.' )
        send_mail('BusBook Nepal - Booked Success',message,'herohiralaal14@gmail.com',[user.email],fail_silently=False)
        messages.success(self.request,'Your bus booked sucessfully! Check your bookings for detail.')
        return HttpResponseRedirect(self.request.path_info)



class BookingList(ListView):
    template_name='booking/your_bookings.html'
    context_object_name = 'booking'
    

    def get_queryset(self):
        user=self.request.user
        queryset = Reservation.objects.filter(user=user).order_by('-id')
        
        return queryset

    def post(self,*args,**kwargs):
        user=self.request.user
        reservationid= self.request.POST.get('reservation')
        reservation=Reservation.objects.get(id=reservationid)
        reservation.cancelled=True
        reservation.save()
        message=('Hello, Dear '+user.first_name + ' ' + user.last_name +' your bus for '+ str(reservation.route) +' on '+ str(reservation.route.date) + ',' + str(reservation.route.time) +' has been cancelled. Thank you.' )
        send_mail('BusBook Nepal - Book Cancelled!',message,'herohiralaal14@gmail.com',[user.email],fail_silently=False)
        messages.success(self.request,'Your cancel request has sucessfully completed.')
    
        return HttpResponseRedirect(self.request.path_info)
