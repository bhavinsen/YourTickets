from django.apps import AppConfig


class TicketshopConfig(AppConfig):
    name = 'ticketshop'

    # def ready(self):
    #     from django.contrib.auth.models import User
    #     from rest_framework.authtoken.models import Token
    #     for user in User.objects.all():
    #         Token.objects.get_or_create(user=user)
