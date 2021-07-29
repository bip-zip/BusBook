
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password

from django.views.generic import View
# from .models import UserProfile
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse


def userlogout(request):
    logout(request)
    return redirect('/')



from django.shortcuts import render
from django.views.generic import TemplateView, View
from .forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import User
from django.conf import settings
from django.http import HttpResponse

# from django.contrib.auth import get_user_model
# User = get_user_model()

# from accounts.tokens import account_activation_token

# Create your views here.


class UserLogin(LoginView):
    template_name = 'bususer/login.html'
    success_url = 'bususer:signup'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'login_active':'active'})
        return context
    


class UserLogoutView(LogoutView):
    success_url = reverse_lazy('accounts:home')
    template_name = 'registration/logged_out'

class UserSignin(CreateView):
    form_class = RegisterForm
    template_name = 'bususer/register.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'signup_active':'active'})
        return context

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #set user to inactive until the email confirmation is sent
            # user = request.user
            user.is_active = False
            user.save()
            #send confirmation email
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('bususer/account_activate_email.html', {
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.id)),
                'token':default_token_generator.make_token(user),
            })
            print(message)
            user.email_user(subject, message, from_email=None, **kwargs)
            messages.success(request, 'Please confirm your email to complete registration')
            return redirect('bususer:login')
        return render(request, self.template_name, {'form':form})

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64)).decode()
            user = User.objects.get(id=uid)
            # print(uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        # User = get_user_model()
        # print(uid)
        # uid = force_text(urlsafe_base64_decode(uidb64))#.decode()
        # # uid = int(uida,10) invalid literal for int() with base 10: b'l\xc4'
        # #the value of uid is b'l\xcc' need to convert this to 1
        # user = User.objects.get(id=uid)
        # # print(uid)

        if user is not None and default_token_generator.check_token(user, token):
            # obj, created = User.objects.get_or_create(user=user)
            user.is_active = True
            user.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request,('Your account have been confirmed.'))
            return redirect('bususer:login')
        else:
            # messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            # return redirect('accounts:activation_invalid')
            return HttpResponse ('The confirmation link was invalid, possibly because it has already been used.')

def activation_sent_view(request):
    return render(request,'bususer/activation_sent.html')

def activation_invalid_view(request):
    return render(request,'bususer/activation_invalid.html')







 
    

        