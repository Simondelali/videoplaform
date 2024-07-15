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
            mail_subject = 'Activate your account.'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol':'https' if request.is_secure() else 'http',
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Account created successfully. Please check your email to verify your account.')
            return render(request, 'users/signup_email_sent.html')
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
                mail_subject = 'Reset your password.'
                message = render_to_string('users/password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https' if request.is_secure() else 'http',
                })
                email = EmailMessage(mail_subject, message, to=[user.email])
                email.send()
            messages.success(request, 'Password reset email has been sent. Please check your inbox.')
            return redirect('password_reset_done')
        else:
            messages.error(request, 'No user found with that email address.')
    return render(request, 'users/password_reset_form.html')
