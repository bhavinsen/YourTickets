from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from datetime import datetime
import datetime, pytz
from yt_dashboard.views.api.event.index import create
from rest_framework.authtoken.models import Token
import json
from ticketshop.views import index
from ticketshop.models import Event
from rest_framework.reverse import reverse
from decimal import Decimal



class BuyTicketViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser1',
            password='testpassword1',
            first_name ='Test',
            last_name ='User',
            is_active=True,
            is_superuser=False
        )
        self.factory = APIRequestFactory()
        self.client = Client()
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
        event_date = current_datetime_utc + datetime.timedelta(hours=-1)
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

        self.data = {
            'header_img': 'null',
            'bg_img': 'null', 
            'primary_color': '#B2283A', 
            'secondary_color': '#53A4BE', 
            'name': 'Test Event', 
            'online': 'true', 
            'event_location': 'Netherlands', 
            'start_date': self.start_date, 
            'end_date': self.end_date, 
            'tickets': f'[{{"name":"Test Ticket","description":"","price":0,"quantity":500,"start_date":"{self.event_start_date}","end_date":"{self.event_end_date}","max_sold":100,"person_amount":0,"start_time":"{self.event_start_time}","end_time":"{self.event_end_time}","persons_per_ticket":1,"amount_per_order":10,"amount":500}}]', 
            'lineup': '[{"id":0,"artist":"Test Artist"}]', 
        }
        self.request = self.factory.post(
            'dashboard2/api/event_create',
            data=self.data,
            format='json'
        )
        force_authenticate(self.request, user=self.user, token=self.user.auth_token)
        self.response = create(self.request)
        self.response_data = json.loads(self.response._container[0])

    def test_buy_ticket_with_valid_data_with_authentication(self):
        user = User.objects.create(
            username='testuser',
            password='testpassword',
            first_name ='Test',
            last_name ='User',
            is_active=True,
            is_superuser=False
        )
        token, _ = Token.objects.get_or_create(user=user)
        event_id = self.response_data['event']['id']
        event_name = self.response_data['event']['name']
        channel_url_name = self.response_data['event']['url']

        event = Event.objects.get(pk=event_id, removed=False)
        self.assertEqual(event.event_public, True)

        event.event_public = True
        event.save()
        self.assertEqual(event.event_public, True)
        
        request = self.factory.get(reverse('buy_ticket', kwargs={'event_id':event_id, 'event_name':event_name}))
        request.session = {}
        request.user = user
        ticketshop_response = index(request,event_id,event_name)

        self.assertEqual(ticketshop_response.status_code, 302)

        data={
            'birth_date':'16-07-1999',
            'postcode':'111222',
            'gender':'M'
        }
        self.client.force_login(user)
        response = self.client.post(ticketshop_response.headers['Location'], data=data)

        self.assertEqual(response.status_code,302)

        next_response = self.client.get(response.headers['Location'])
        context = next_response.context

        #User test
        self.assertEqual(context[0]['user'].username, user.username)
        self.assertEqual(context[0]['user'].is_authenticated, True)
        self.assertEqual(context[0]['user'].is_active, True)
        self.assertEqual(context[0]['user'].is_superuser, False)

        #Event test
        self.assertEqual(context[0]['cur_event'].id, self.response_data['event']['id'])
        self.assertEqual(context[0]['cur_event'].title, self.response_data['event']['title'])
        self.assertEqual(context[0]['cur_event'].location, self.response_data['event']['location'])
        self.assertEqual(context[0]['cur_event'].total_service_costs_gross, Decimal(self.response_data['event']['total_service_costs_gross']))
        self.assertEqual(context[0]['cur_event'].removed, self.response_data['event']['removed'])
        self.assertEqual(context[0]['cur_event'].start_date.strftime('%Y-%m-%d'), self.response_data['event']['start_date'])
        self.assertEqual(context[0]['cur_event'].end_date.strftime('%Y-%m-%d'), self.response_data['event']['end_date'])

        #Lineup test
        self.assertEqual(context[0]['lineup'][0].id, self.response_data['lineups'][0]['id'])
        self.assertEqual(context[0]['lineup'][0].artist, self.response_data['lineups'][0]['artist'])

        #Tickets test
        self.assertEqual(context[0]['tickets'][0].id, self.response_data['tickets'][0]['pk'])
        self.assertEqual(context[0]['tickets'][0].price, self.response_data['tickets'][0]['price'])
        self.assertEqual(context[0]['tickets'][0].quantity, self.response_data['tickets'][0]['quantity'])
        self.assertEqual(context[0]['tickets'][0].deleted, False)
        self.assertEqual(context[0]['tickets'][0].name, self.response_data['tickets'][0]['name'])


    def test_buy_ticket_with_get_request(self):
        user = User.objects.create(
            username='testuser',
            password='testpassword',
            first_name ='Test',
            last_name ='User',
            is_active=True,
            is_superuser=False
        )
        token, _ = Token.objects.get_or_create(user=user)
        event_id = self.response_data['event']['id']
        event_name = self.response_data['event']['name']

        event = Event.objects.get(pk=event_id, removed=False)
        self.assertEqual(event.event_public, True)

        event.event_public = True
        event.save()
        self.assertEqual(event.event_public, True)

        self.client.force_login(user)
        request = self.factory.get(reverse('buy_ticket', kwargs={'event_id':event_id, 'event_name':event_name}))
        request.session = {}
        request.user = user
        ticketshop_response = index(request,event_id,event_name)
        

        self.assertEqual(ticketshop_response.status_code, 302)

        next = f'/ticketshop/{event_id}/{event_name}/'
        
        response = self.client.get(ticketshop_response.headers['Location'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0]['next'], next)



