from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.forms import RegisterForm, BonusForm, UseBonusForm, EmailLoginForm
from accounts.models import BonusTransaction
from decimal import Decimal

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='TestPassword123',
            first_name='Імʼя',
            last_name='Прізвище',
            phone_number='1234567890'
        )

    def test_user_created(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('TestPassword123'))

    def test_user_str(self):
        self.assertEqual(str(self.user), 'test@example.com')


class BonusTransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='bonus@example.com',
            password='TestPass123',
            phone_number='1111111111'
        )
        self.transaction = BonusTransaction.objects.create(
            user=self.user,
            order_amount=Decimal('100.00'),
            bonus_awarded=Decimal('5.00')
        )

    def test_transaction_str(self):
        self.assertIn(str(self.transaction.bonus_awarded), str(self.transaction))
        self.assertIn(self.user.email, str(self.transaction))


class RegisterFormTest(TestCase):
    def test_valid_form(self):
        form = RegisterForm(data={
            'first_name': 'Імʼя',
            'last_name': 'Прізвище',
            'email': 'valid@example.com',
            'phone_number': '1234567890',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!'
        })
        self.assertTrue(form.is_valid())

    def test_email_exists(self):
        User.objects.create_user(email='taken@example.com', password='123', phone_number='0000000000')
        form = RegisterForm(data={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'taken@example.com',
            'phone_number': '1231231234',
            'password1': 'somepass123',
            'password2': 'somepass123'
        })
        self.assertFalse(form.is_valid())


class BonusFormTest(TestCase):
    def test_valid_bonus_form(self):
        form = BonusForm(data={'order_amount': '150.00'})
        self.assertTrue(form.is_valid())


class UseBonusFormTest(TestCase):
    def test_valid_use_bonus_form(self):
        form = UseBonusForm(data={'bonus_amount': '10.00'})
        self.assertTrue(form.is_valid())


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='login@test.com',
            password='pass12345',
            phone_number='0000000000'
        )

    def test_login_view_valid(self):
        response = self.client.post(reverse('accounts:login'), {
            'email': 'login@test.com',
            'password': 'pass12345'
        })
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_email(self):
        response = self.client.post(reverse('accounts:login'), {
            'email': 'invalid@email.com',
            'password': 'pass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign In")


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='profile@test.com',
            password='Test1234',
            phone_number='1111111111'
        )

    def test_profile_view_requires_login(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)  # redirects to login

    def test_profile_view_logged_in(self):
        self.client.login(email='profile@test.com', password='Test1234')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
