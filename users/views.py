from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import CustomUserCreationForm
from .models import CustomUser
from .tokens import account_activation_token
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.urls import reverse
from trycourier import Courier
from dotenv import load_dotenv
import os

load_dotenv()

User = get_user_model()

@ensure_csrf_cookie
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            
            # Construct the activation link
            activation_link = request.build_absolute_uri(
                reverse('activate', kwargs={'uidb64': uid, 'token': token})
            )


            # Initialize Courier client
            client = Courier(auth_token=os.environ['auth_token'])

            # Send email using Courier
            resp = client.send_message(
                message={
                    "to": {
                        "email": form.cleaned_data.get('email'),
                    },
                    "template": "7CGAQ95SF0MBA0GTFG4C6P8EYY13",
                    "data": {
                        "recipientName": user.email,
                        "activationLink": activation_link,
                    },
                }
            )

            if resp['requestId']:
                messages.success(request, 'Account created successfully. Please check your email to verify your account.')
                return render(request, 'users/signup_email_sent.html')
            else:
                messages.error(request, 'There was an error sending the activation email. Please try again.')
        else:
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been successfully activated. You can now log in.')
        return redirect('login')
    else:
        return render(request, 'users/activation_invalid.html')
  
def home(request):
    return render(request, 'home.html') 

def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')

def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                current_site = get_current_site(request)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                
                # Construct the password reset link
                reset_link = request.build_absolute_uri(
                    reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )

                # Initialize Courier client
                client = Courier(auth_token=os.environ['auth_token'])

                # Send email using Courier
                resp = client.send_message(
                    message={
                        "to": {
                            "email": user.email,
                        },
                        "template": "Y9Z19C9D774624H0AB1RRG1D3R0W",
                        "data": {
                            "recipientName": user.email,
                            "resetLink": reset_link,
                        },
                    }
                )

                if resp['requestId']:
                    messages.success(request, 'Password reset email has been sent. Please check your inbox.')
                else:
                    messages.error(request, 'There was an error sending the password reset email. Please try again.')
            
            return redirect('password_reset_done')
        else:
            messages.error(request, 'No user found with that email address.')
    return render(request, 'users/password_reset_form.html')