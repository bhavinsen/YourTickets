from django.contrib.auth.models import User, Group
from ticketshop.models import Event, EventOrganiser, SoldTicket
from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer):
	id = serializers.ReadOnlyField()
	class Meta:
		model = Event
		fields = ('id', 'title', 'location', 'description', 'start_date', 'end_date', 'service_cost', 'event_public', 'unique_tickets')
		
class TicketSerializer(serializers.ModelSerializer):
	class Meta:
		model = SoldTicket
		fields = ('ticket_gen_id', 'first_name', 'last_name', 'checked')