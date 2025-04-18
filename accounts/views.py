from decimal import Decimal, ROUND_DOWN

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from accounts.forms import EmailLoginForm, RegisterForm, BonusForm
from accounts.models import User
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import io
import qrcode
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.core.signing import Signer, BadSignature

signer = Signer()


@login_required
def profile_page_view(request):
    return render(request, 'accounts/profile.html')

class QrPageView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/qr-code.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['signed_user_id'] = signer.sign(self.request.user.id)
        return ctx

def qrcode_view(request, signed_user_id):
    try:
        user_id = signer.unsign(signed_user_id)
        user = User.objects.get(pk=user_id)
    except (BadSignature, User.DoesNotExist):
        raise Http404("Неправильний QR‑код")

    redeem_url = request.build_absolute_uri(
        reverse('accounts:redeem', args=[signed_user_id])
    )

    img = qrcode.make(redeem_url)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')

@login_required
@permission_required('accounts.can_redeem_bonus', raise_exception=True)
def redeem_bonus(request, signed_user_id):
    try:
        user_id = signer.unsign(signed_user_id)
        user = User.objects.get(pk=user_id)
    except (BadSignature, User.DoesNotExist):
        raise Http404("Неправильний QR‑код")

    if request.method == 'POST':
        form = BonusForm(request.POST)
        if form.is_valid():
            amt = form.cleaned_data['order_amount']
            percent = Decimal('0.05')
            bonus = (amt * percent).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
            user.bonuses += bonus
            user.save()
            user.bonus_transactions.create(
                order_amount=amt,
                bonus_awarded=bonus
            )
            return render(request, 'accounts/redeem_success.html', {
                'user': user,
                'order_amount': amt,
                'bonus': bonus
            })
    else:
        form = BonusForm()

    return render(request, 'accounts/redeem.html', {
        'form': form,
        'user': user
    })

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