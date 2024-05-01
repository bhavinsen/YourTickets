# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from dashboard.common.validators.ImageValidator import ImageDimensionsValidator, FileExtensionValidator
from django.contrib.auth.models import AbstractUser

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



class Event(models.Model):
    def __str__(self):
        return self.title

    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    start_date = models.DateTimeField('date started', blank=True)
    end_date = models.DateTimeField('date ended', blank=True)
    service_cost = models.IntegerField()
    event_public = models.BooleanField()
    unique_tickets = models.BooleanField()
    event_url = models.CharField(max_length=200, default='')
    views = models.IntegerField(default=0)
    marked = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)
    show_covid19_info = models.BooleanField(default=False)
    online = models.BooleanField(default=False)

    service_cost_discount_cents = models.IntegerField(default=0)
    ticket_amount = models.IntegerField(default=0)
    total_tickets = models.IntegerField(default=0)
    total_person_amount = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_service_costs =models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_service_costs_discount =models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_service_costs_gross =models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __unicode__(self):
        return u'%s' % self.title

    def get_tickets(self):
        tickets = Ticket.objects.filter(event_id=self.id, deleted=False).order_by('pk')

        return tickets

    def update_tickets_totals(self):
        tickets = Ticket.objects.filter(event_id=self.id, deleted=False).order_by('pk')
        event_ticket_amount = 0
        event_total_tickets = 0
        event_total_person_amount = 0
        event_total_price = 0
        event_total_service_costs = 0
        event_total_service_costs_discount = 0
        event_total_service_costs_gross = 0


        for ticket in tickets:
            event_ticket_amount += 1
            event_total_tickets += ticket.quantity
            event_total_person_amount += ticket.total_person_amount
            event_total_price += ticket.total
            event_total_service_costs += ticket.service_costs
            event_total_service_costs_discount += ticket.service_costs_discount
            event_total_service_costs_gross += ticket.service_costs_gross
        
        self.ticket_amount = event_ticket_amount
        self.total_tickets = event_total_tickets
        self.total_person_amount = event_total_person_amount
        self.total_price = event_total_price
        self.total_service_costs = event_total_service_costs
        self.total_service_costs_discount = event_total_service_costs_discount
        self.total_service_costs_gross = event_total_service_costs_gross

        self.save(update_fields=['ticket_amount',
                                'total_tickets', 
                                'total_person_amount',
                                'total_price',
                                'total_service_costs',
                                'total_service_costs_discount',
                                'total_service_costs_gross'])

class TicketShopCustom(models.Model):
    def __str__(self):
        return self.event_id.title

    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    primary_color = models.CharField(max_length=7)
    secondary_color = models.CharField(max_length=7)
    # ImageDimensionsValidator(min_height=100000)
    header_img = models.ImageField(
        upload_to='images/event/',
        default='images/event/header.jpg',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
            # ImageDimensionsValidator(dimensions=[(727, 725)])
        ]
    )
    bg_img = models.ImageField(
        upload_to='images/event/',
        default='images/event/bg.jpg',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            # ImageDimensionsValidator(dimensions=[(3000, 2000)])
        ]
    )


class Iframe(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)


class Languages(models.Model):
    def __str__(self):
        return self.language_name + " - " + self.language_code

    language_code = models.CharField(max_length=10)
    language_name = models.CharField(max_length=100)


class Dictionary(models.Model):
    def __str__(self):
        return self.language.language_code + " - " + self.name

    language = models.ForeignKey(Languages, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)


class UserExtra(models.Model):
    def __str__(self):
        return str(self.user)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        default=1
    )

    ################################################################################################
    #############					DEFAULT datetime.now not working yet, CRASH 		############
    #############						Probeer de standaard user van python			############
    #############						te extenden met extra data						############
    ################################################################################################
    birth_date = models.DateField('birth date')

    SEX_CHOICES = (('M', 'Man'), ('F', 'Vrouw'))

    sex = models.CharField(max_length=1, default='N', choices=SEX_CHOICES)

    adress = models.CharField(max_length=200, default='')

    is_organizer = models.BooleanField(default=False)
    is_visitor = models.BooleanField(default=True)
    activate_token = models.CharField(max_length=255, default='')
    terms_agreed = models.BooleanField(default=False)
    avatar = models.ImageField(
        upload_to='images/user/',
        default='images/user/default_avatar.png',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
            # ImageDimensionsValidator(dimensions=[(727, 725)])
        ]
    )


class LineUp(models.Model):
    def __str__(self):
        return self.artist

    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)

    artist = models.CharField(max_length=200)
    url = models.CharField(max_length=300)


class UserExtraSeller(models.Model):
    def __str__(self):
        return self.event_id.title

    event_id = models.ForeignKey(Event, null=True, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)

    kvk_number = models.CharField(max_length=30, default='')
    rekening_number = models.CharField(max_length=30, default='')
    factuur_adress = models.CharField(max_length=200, default='')
    rekening_houder = models.CharField(max_length=200, default='')
    btw_nr = models.CharField(max_length=200, default='')
    postal_code = models.CharField(max_length=6, default='')
    house_number = models.CharField(max_length=6, default='')
    house_number_addition = models.CharField(max_length=6, default='')
    company_name = models.CharField(max_length=200, default='')
    big = models.CharField(max_length=200, default='')


class EventOrganiser(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)

    # ADMIN_CHOICES = ((0, 'Geen rechten'), (1, 'Halve rechten'), (2, 'Alle rechten'))

    ROLE_OWNER = 2
    ROLE_ADMINISTRATOR = 1
    ROLE_VIEW = 0

    ROLES = (
        (ROLE_ADMINISTRATOR, 'Beheerder'),
        (ROLE_VIEW, 'View'),
        # everybody allready has number 2, so this NEEDS to be in 3th position
        (ROLE_OWNER, 'Owner'),
    )

    admin_rights = models.IntegerField(default=0, choices=ROLES)

    def __str__(self):
        return '{0} - {1}'.format(self.event.title,  self.user.email)
# userextraseller event_id doesnt make any sense
# that column needs to be checkout out of the usage

# def test():
#     for user in User:
#         user_extra = UserExtra.objects.get(user=user)
#         if user_extra.is_organizer:
#             # add user to auth group organizer
#             user_extra_seller = UserExtraSeller.objects.get(user=user)
#
#             # migrate these fields to userprofile:
#             # kvk_number = models.CharField(max_length=30, default='')
#             # rekening_number = models.CharField(max_length=30, default='')
#             # factuur_adress = models.CharField(max_length=200, default='')
#             # rekening_houder = models.CharField(max_length=200, default='')
#             # btw_nr = models.CharField(max_length=200, default='')
#             # postal_code = models.CharField(max_length=6, default='')
#             # house_number = models.CharField(max_length=6, default='')
#             # house_number_addition = models.CharField(max_length=6, default='')
#             # company_name = models.CharField(max_length=200, default='')
#             # big = models.CharField(max_length=200, default='')
#
#             EventOrganiser.objects.filter(user=user)
#             pass
#         elif user_extra.is_visitor:
#             # add user to auth group visitor
#             # if soldticket doesnt have an user_id ....
#             pass
#         shared_events_for_user = SharedEvents.objects.filter(user=user)
#         # insert into EventOrganiser where role = view

# this is allready in the user model:
# first_name
# last_name
# email
# username

# questions:
# maybe business contact person toevoegen?
# gebruikers koppelen aan events organizer?
# class UserProfile(models.Model):
#     GENDER_CHOICES = (('m', 'Man'), ('f', 'Vrouw'))
#
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     # personal info
#
#     birthdate = models.DateField()
#     gender = models.CharField(max_length=1, default='u', choices=GENDER_CHOICES)
#     phone_number = models.CharField(max_length=30, default='')
#
#     # personal location info
#     street_name = models.CharField(max_length=30, default='')
#     street_number = models.CharField(max_length=30, default='')
#     street_number_addition = models.CharField(max_length=30, default='')
#     postal_code = models.CharField(max_length=30, default='')
#
#     # business general info
#     company_name = models.CharField(max_length=200, default='')
#     business_phone_number = models.CharField(max_length=30, default='')
#
#     # business account info
#     coc_number = models.CharField(max_length=30, default='')
#     bank_account_number = models.CharField(max_length=30, default='')
#     bank_account_holder = models.CharField(max_length=200, default='')
#     tax_nr = models.CharField(max_length=200, default='')
#     big = models.CharField(max_length=200, default='')
#
#     # business location info
#     business_street_name = models.CharField(max_length=200, default='')
#     business_street_number = models.CharField(max_length=30, default='')
#     business_street_number_addition = models.CharField(max_length=30, default='')
#     business_postal_code = models.CharField(max_length=30, default='')
#
#     # functional info
#     activate_token = models.CharField(max_length=255, default='')
#     terms_agreed = models.BooleanField(default=False)
#
#     # settings
#     avatar = models.ImageField(
#         upload_to='images/user/',
#         default='images/user/default_avatar.png',
#         validators=[
#             FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
#             # ImageDimensionsValidator(dimensions=[(727, 725)])
#         ]
#     )





class Ticket(models.Model):
    def __str__(self):
        return self.event.title + " - " + self.name

    def __unicode__(self):
        return u'%s - %s' % (self.event.title, self.name)

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    price = models.IntegerField()
    quantity = models.IntegerField()

    start_date = models.DateTimeField('date started', blank=True)
    end_date = models.DateTimeField('date ended', blank=True)

    max_sold = models.IntegerField(default='10')
    deleted = models.BooleanField(default=False)

    person_amount = models.IntegerField(default='1')
    service_costs_gross = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_costs_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_costs = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_person_amount = models.IntegerField(default='0')

    def update_totals(self):
        from yourtickets.common import shop
        event = Event.objects.filter(pk=self.event_id).first()

        self.total = (self.price /100)  * float(self.quantity)
        self.total_person_amount = int(self.person_amount) * int(self.quantity)

        self.service_costs = shop.get_service_cost(self.total , int(self.quantity) , event.service_cost_discount_cents)
        self.service_costs_gross = shop.get_service_cost(self.total , int(self.quantity) , event.service_cost_discount_cents)
        self.service_costs_discount = self.service_costs_gross - self.service_costs

        self.save(update_fields=['total', 
                                'total_person_amount',
                                'service_costs',
                                'service_costs_discount',
                                'service_costs_gross'])

class Saleschannel(models.Model):
    name = models.CharField(max_length=200, default='')
    url_name = models.CharField(max_length=100, default='')
    event = models.ForeignKey(Event, blank=False, on_delete=models.DO_NOTHING)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.name


class Order(models.Model):
    def __str__(self):
        return str(self.id)

    user = models.ForeignKey(User, default=1, on_delete=models.DO_NOTHING)
    mollie_id = models.CharField(max_length=100, default="")
    order_paid = models.BooleanField(default=False)
    date = models.DateTimeField('Order creation date', auto_now_add=True, blank=True)
    mail_send = models.BooleanField(default=False)
    email_allowed = models.BooleanField(default=False)
    ordered_in_language = models.CharField(max_length=10, default="unknown")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_costs = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=200, default="")
    ga_tracked = models.BooleanField(default=False)
    sale_channel = models.ForeignKey(Saleschannel, null=True, blank=True, on_delete=models.DO_NOTHING)
    agreed_covid19_info = models.CharField(blank=True, null=True, max_length=5)
    uid = models.CharField(blank=True, default='', max_length=32)
    event = models.ForeignKey(Event, null=True, on_delete=models.DO_NOTHING)
    service_costs_gross = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_costs_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    person_amount = models.IntegerField(default='0')
    sold_tickets = models.IntegerField(default='0')

class GuestTickets(models.Model):
    hash = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    delayed_send = models.BooleanField(default=False)
    type = models.CharField(max_length=50, null=True, blank=True, default='')

class SoldTicket(models.Model):
    def __str__(self):
        return str(self.ticket_gen_id) + " - " + str(self.order_nr)

    ticket_gen_id = models.BigIntegerField()

    ticket_type = models.ForeignKey(Ticket, null=True, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, null=True, on_delete=models.DO_NOTHING)

    order_nr = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)

    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)

    sold_date = models.DateTimeField('date sold', auto_now_add=True, blank=True)

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    birth_date = models.DateField('birth date', default=datetime.now, blank=True, null=True)

    SEX_CHOICES = (('M', 'Man'), ('F', 'Vrouw'), ('X', 'X'), ('U', 'Unknown'))

    sex = models.CharField(max_length=1, default='N', choices=SEX_CHOICES)

    adress = models.CharField(max_length=200, default='')

    checked = models.BooleanField(default=False)
    email_allowed = models.BooleanField(default=False)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    is_subticket = models.BooleanField(default=False)

    primary_ticket = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)

    email = models.CharField(max_length=200, default='')

    is_guest_ticket = models.BooleanField(default=False)

    is_special_guest_ticket = models.BooleanField(default=False)

    guest_ticket = models.ForeignKey(GuestTickets, null=True, blank=True, on_delete=models.CASCADE)

    service_costs_gross = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_costs_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)    
    service_costs = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class accessRequests(models.Model):
    def __str__(self):
        return self.email

    sold_date = models.DateTimeField('date sold', auto_now_add=True, blank=True)
    email = models.CharField(max_length=200, default='')


class Log(models.Model):
    category = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=False)


class Orderlog(models.Model):

    TYPE_BEFORE_MOLLIE_AANVRAAG = 'BEFORE_MOLLIE_AANVRAAG'

    TYPE_WEBHOOK_MOLLIE_API_RECEIVED = 'WEBHOOK_MOLLIE_API_RECEIVED'
    TYPE_WEBHOOK_MOLLIE_ORDER_OK = 'WEBHOOK_MOLLIE_ORDER_OK'
    TYPE_WEBHOOK_MOLLIE_API_ERROR = 'WEBHOOK_MOLLIE_API_ERROR'
    TYPE_WEBHOOK_MOLLIE_EXCEPTION = 'WEBHOOK_MOLLIE_EXCEPTION'
    TYPE_WEBHOOK_MOLLIE_OK = 'WEBHOOK_MOLLIE_OK'

    TYPE_MAIL_PDF_CREATED = 'MAIL_PDF_CREATED'
    TYPE_MAIL_PDF_ERROR = 'MAIL_PDF_ERROR'
    TYPE_MAIL_SEND = 'TYPE_MAIL_SEND'

    TYPE_TASK_MANAGER_START = 'TASK_MANAGER_START'
    TYPE_TASK_MANAGER_DONE = 'TASK_MANAGER_DONE'

    TYPE_DONE = 'TYPE_DONE'

    TYPES = (
        (TYPE_BEFORE_MOLLIE_AANVRAAG, TYPE_BEFORE_MOLLIE_AANVRAAG),
        (TYPE_WEBHOOK_MOLLIE_API_RECEIVED, TYPE_WEBHOOK_MOLLIE_API_RECEIVED),
        (TYPE_WEBHOOK_MOLLIE_ORDER_OK, TYPE_WEBHOOK_MOLLIE_ORDER_OK),
        (TYPE_WEBHOOK_MOLLIE_API_ERROR, TYPE_WEBHOOK_MOLLIE_API_ERROR),
        (TYPE_WEBHOOK_MOLLIE_EXCEPTION, TYPE_WEBHOOK_MOLLIE_EXCEPTION),
        (TYPE_WEBHOOK_MOLLIE_OK, TYPE_WEBHOOK_MOLLIE_OK),
        (TYPE_MAIL_PDF_CREATED, TYPE_MAIL_PDF_CREATED),
        (TYPE_MAIL_PDF_ERROR, TYPE_MAIL_PDF_ERROR), 
        (TYPE_MAIL_SEND, TYPE_MAIL_SEND), 
        (TYPE_DONE, TYPE_DONE),
        (TYPE_TASK_MANAGER_START, TYPE_TASK_MANAGER_START),
        (TYPE_TASK_MANAGER_DONE, TYPE_TASK_MANAGER_DONE),
    )

    date = models.DateTimeField(auto_now_add=True, blank=False)
    mollie_id = models.TextField(blank=True)
    order_id = models.TextField(blank=True)
    
    description = models.TextField(blank=True)
    type = models.CharField(
        max_length=50,
        choices=TYPES,
        default='UNKNOWN',
    )


class Multiticketshop(models.Model):
    name = models.CharField(max_length=200, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    use_in_iframe = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s - %s' % (self.user, self.name)


class DynamicUrl(models.Model):

    EVENT = 'EVENT'
    MULTITICKETSHOP = 'MULTITICKETSHOP'
    SALESCHANNEL = 'SALESCHANNEL'

    TYPES = (
        (EVENT, 'Event'),
        (MULTITICKETSHOP, 'Multi ticket shop'),
    )

    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.DO_NOTHING)

    multiticketshop = models.ForeignKey(Multiticketshop, null=True, blank=True, on_delete=models.DO_NOTHING,)

    url_name = models.CharField(max_length=200)
    enabled = models.BooleanField(default=True)
    type = models.CharField(
        max_length=50,
        choices=TYPES,
        default='EVENT',
    )


class MultiticketshopEvents(models.Model):
    multiticketshop = models.ForeignKey(Multiticketshop, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
    order = models.IntegerField()


class EventPayments(models.Model):
    BLANK           = ''
    PARTIAL_PAYMENT = 'PARTIAL-PAYMENT'
    FINAL_PAYMENT   = 'FINAL-PAYMENT'
    REFUNDS         = 'REFUNDS'
    CHARGE          = 'CHARGE'

    TYPES = (
        (BLANK, ''),
        (PARTIAL_PAYMENT , 'Partial payment'),
        (FINAL_PAYMENT   , 'Final payment'),
        (REFUNDS         , 'Refunds'),
        (CHARGE          , 'Charge'),
    )


    user = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, null=True, blank=True, default=None, on_delete=models.DO_NOTHING)
    payout_date = models.DateTimeField('date sold', blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.CharField(max_length=200, default='')
    approved = models.BooleanField(default=True)
    type = models.CharField(
        max_length=50,
        choices=TYPES,
        default='',
    )

class SharedEvents(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class TempSharedEvents(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_email = models.CharField(max_length=200, default='')


class PageViews(models.Model):
    uuid = models.CharField(max_length=200, default='')
    ip = models.CharField(max_length=200, default='')
    url = models.TextField()
    date = models.DateTimeField(auto_now_add=True, blank=True)
    # charfield or not?
    event_id = models.CharField(max_length=200, default='')


class PreReg(models.Model):
    first_name = models.CharField(max_length=200, default='')
    last_name = models.CharField(max_length=200, default='')
    email = models.CharField(max_length=200, default='')
    phone_number = models.CharField(max_length=200, default='')
    country = models.CharField(max_length=200, default='')
    notify_me = models.BooleanField()