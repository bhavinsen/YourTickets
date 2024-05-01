from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from yourtickets.forms import RegisterForm
from .views import login_req
from .views import register_req

class LoginFuncTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.test_user = User.objects.create(
            username='testuser',
            password='testpassword',
            first_name ='Test',
            last_name ='User',
            is_active=True,
            is_superuser=False
        )
        self.factory = RequestFactory()

    def test_login_successful(self):
        # Create a POST request with valid login credentials
        request = self.factory.post(reverse('login'), data={'username': ['testuser'], 'password': ['testpassword']})
        request.user = self.test_user
        self.assertEqual(request.user, self.test_user)

        response = login_req(request)
        self.assertEqual(response.status_code, 200)

    def test_login_failed(self):
        # Create a POST request with invalid login credentials
        request = self.factory.post(reverse('login'), data={'username': ['invaliduser'], 'password': ['invalidpassword']})
        request.user = self.test_user
        self.assertEqual(request.user, self.test_user)
        response = login_req(request)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(request.user)

    def test_login_empty_credentials(self):
        # Create a POST request with empty login credentials
        request = self.factory.post(reverse('login'), data={'username': [''], 'password': ['']})
        request.user = self.test_user

        response = login_req(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(request.user)

class RegisterFuncTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_register_successful(self):
        # Create a POST request with valid registration data
        request = self.factory.post(reverse('register'), data={'username': ['demo1@test.com'], 'password': ['test1password'], 'first_name': ['test1'], 'last_name': ['user1']})
        register_form = RegisterForm(request.POST)

        self.assertTrue(register_form.is_valid())

        # Create the user
        response = register_req(request)

        self.assertEqual(response.status_code, 200)

        # Check if the user is created

        user = User.objects.get(username='demo1@test.com')
        self.assertEqual(user.username, 'demo1@test.com')
        self.assertEqual(user.first_name, 'test1')
        self.assertEqual(user.last_name, 'user1')

    def test_register_invalid_username(self):
        # Create a POST request with invalid username
        
        request = self.factory.post(
            reverse('register'), 
            data={'username': [''], 
                  'password': ['testpassword'], 
                  'first_name': ['Test'], 
                  'last_name': ['User']
                  })

        register_form = RegisterForm(request.POST)

        # Check if the form is not valid
        self.assertFalse(register_form.is_valid())

        # Check the error message
        self.assertEqual(register_form.errors['username'][0], 'Dit veld is vereist.')


    def test_register_invalid_password(self):
        # Create a POST request with invalid password
        request = self.factory.post(
            reverse('register'),
            data={'username': ['testuser1'], 
                  'password': [''], 
                  'first_name': ['Test1'], 
                  'last_name': ['User1']
                  })
        register_form = RegisterForm(request.POST)

        self.assertFalse(register_form.is_valid())

        # Check the error message
        self.assertEqual(register_form.errors['password'][0], 'Dit veld is vereist.')



