from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from datetime import datetime
import datetime, pytz
from yt_dashboard.views.api.event.index import create
from rest_framework.authtoken.models import Token
import json


class CreateEventViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='testuser1',
            password='testpassword1',
            first_name ='Test',
            last_name ='User',
            is_active=True,
            is_superuser=False
        )
        self.factory = APIRequestFactory()
        self.token, _ = Token.objects.get_or_create(user=self.user)

        current_datetime_utc = datetime.datetime.utcnow()
        #start_date
        tomorrow_date = current_datetime_utc + datetime.timedelta(days=1)
        desired_timezone = pytz.timezone(settings.TIME_ZONE)
        current_datetime_in_desired_timezone = tomorrow_date.replace(tzinfo=pytz.utc).astimezone(desired_timezone)
        self.start_date = current_datetime_in_desired_timezone.strftime("%Y-%m-%d %H:%M")

        #end_date
        tomorrow_date = current_datetime_utc + datetime.timedelta(days=1, hours=2)
        desired_timezone = pytz.timezone(settings.TIME_ZONE)
        current_datetime_in_desired_timezone = tomorrow_date.replace(tzinfo=pytz.utc).astimezone(desired_timezone)
        self.end_date = current_datetime_in_desired_timezone.strftime("%Y-%m-%d %H:%M")

        # Event start time
        event_date = current_datetime_utc + datetime.timedelta(days=1,hours=2)
        desired_timezone = pytz.timezone(settings.TIME_ZONE)
        current_time_with_timezone = event_date.astimezone(desired_timezone)
        self.event_start_time = current_time_with_timezone.strftime('%H:%M')
        self.event_start_date = current_time_with_timezone.strftime('%Y-%m-%d')

        # Event End time
        event_date = current_datetime_utc + datetime.timedelta(days=1,hours=5)
        desired_timezone = pytz.timezone(settings.TIME_ZONE)
        current_time_with_timezone = event_date.astimezone(desired_timezone)
        self.event_end_time = current_time_with_timezone.strftime('%H:%M')
        self.event_end_date = current_time_with_timezone.strftime('%Y-%m-%d')

    def test_create_event_with_valid_data(self):
        data = {
            'header_img': 'null',
            'bg_img': 'null', 
            'primary_color': '#B2283A', 
            'secondary_color': '#53A4BE', 
            'name': 'Test Event', 
            'online': 'false', 
            'event_location': 'Netherlands', 
            'start_date': self.start_date, 
            'end_date': self.end_date, 
            'tickets': f'[{{"name":"Test Ticket","description":"","price":23,"quantity":236,"start_date":"{self.event_start_date}","end_date":"{self.event_end_date}","max_sold":10,"person_amount":1,"start_time":"{self.event_start_time}","end_time":"{self.event_end_time}","persons_per_ticket":1,"amount_per_order":10,"amount":236}}]', 
            'lineup': '[{"id":0,"artist":"Test Artist"}]', 
        }
        request = self.factory.post(
            'dashboard2/api/event_create',
            data=data,
            format='json'
        )
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = create(request)
        response_data = json.loads(response._container[0])
        event_data = response_data.get('event', None)
        lineups_data = response_data.get('lineups', None)
        tickets_data = response_data.get('tickets', None)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(event_data['title'], 'Test Event')
        self.assertEqual(tickets_data[0]['name'], 'Test Ticket')
        self.assertEqual(lineups_data[0]['artist'], 'Test Artist')

    def test_create_event_without_authentication(self):
        data = {
            'header_img': 'null',
            'bg_img': 'null', 
            'primary_color': '', 
            'secondary_color': '', 
            'name': 'Test Event', 
            'online': 'false', 
            'event_location': '', 
            'start_date': self.start_date, 
            'end_date': self.end_date, 
            'tickets': f'[{{"name":"Test Ticket","description":"","price":23,"quantity":236,"start_date":"{self.event_start_date}","end_date":"{self.event_end_date}","max_sold":10,"person_amount":1,"start_time":"{self.event_start_time}","end_time":"{self.event_end_time}","persons_per_ticket":1,"amount_per_order":10,"amount":236}}]', 
            'lineup': '[{"id":0,"artist":"Test Artist"}]', 
        }

        request = self.factory.post(
            'dashboard2/api/event_create',
            data=data,
            format='json'
        )
        response = create(request)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Authenticatiegegevens zijn niet opgegeven.')

    def test_create_event_with_invalid_data(self):
        data = {
            'header_img': 'null',
            'bg_img': 'null', 
            'primary_color': '#B2283A', 
            'secondary_color': '#53A4BE', 
            'name': 'Test Event', 
            'online': 'false', 
            'event_location': 'Netherlands', 
            'start_date': 'self.start_date', 
            'end_date': 'self.end_date', 
            'tickets': f'[{{"name":"Test Ticket","description":"","price":23,"quantity":236,"start_date":"{self.event_start_date}","end_date":"{self.event_end_date}","max_sold":10,"person_amount":1,"start_time":"{self.event_start_time}","end_time":"{self.event_end_time}","persons_per_ticket":1,"amount_per_order":10,"amount":236}}]', 
            'lineup': '[{"id":0,"artist":"Test Artist"}]', 
        }

        request = self.factory.post(
            'dashboard2/api/event_create',
            data=data,
            format='json'
        )
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = create(request)
        response_data = json.loads(response._container[0])
        errors = response_data['errors'][0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(errors['errors']['start_date'], ["Voer een geldige datum/tijd in."])
        self.assertEqual(errors['errors']['end_date'], ["Voer een geldige datum/tijd in."])



