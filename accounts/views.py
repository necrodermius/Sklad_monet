from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from accounts.forms import EmailLoginForm, RegisterForm
from accounts.models import User


# Create your views here.
@login_required
def profile_page_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def qrcode_view(request):
    return render(request, 'accounts/qr-code.html')

def login_view(request):
    form = EmailLoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        try:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
            else:
                messages.error(request, "Неправильний пароль.")
        except User.DoesNotExist:
            messages.error(request, "Користувача з таким email не існує.")

    return render(request, "registration/login.html", {"form": form})


class RegisterView(FormView):
    model = User
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)