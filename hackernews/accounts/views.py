from django.shortcuts import render, redirect
from django.views import generic 
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

# Create your views here.


class UserRegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    
    success_url = reverse_lazy('login')


def logout_user(request):
    
    logout(request)
    
    return redirect('login')