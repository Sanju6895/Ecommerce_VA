from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.http import HttpResponse
from .forms import RegistrationForm, UserEditForm
from .token import account_activation_token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import UserBase
from orders.views import user_orders

def account_register(request):

    if request.user.is_authenticated:
        return redirect("account:dashboard")

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False #Will send email to verify the user and then make them active
            user.save()

            #setup email
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            print(message)
            #user.email_user(subject=subject, message=message)
            return HttpResponse('Account Created, Activation Code Sent on Email')

    else:
        registerForm = RegistrationForm()
    context = {'form': registerForm}    
    return render(request, 'account/register.html', context)


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request,user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/activation_invalid.html')

@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/edit_details.html', {'user_form': user_form})

@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')
    

@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request,
                  'account/dashboard.html',
                  {'section': 'profile', 'orders': orders})