from django.shortcuts import render, redirect

# Create your views here.
from .forms import RegistrationForm

def account_register(request):

    if request.user.is_authenticated():
        return redirect("")

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False #Will send email to verify the user and then make them active
            user.save()

    