import json
import datetime

from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
# from django.utils.translation import gettext as _
from django.core.mail import EmailMessage
from django.contrib.auth import logout as lgout
from django.db.models import Sum
from django.templatetags.static import static

from ticketshop.models import UserExtra, EventPayments, Event, Ticket, SoldTicket, UserExtraSeller
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from yt_dashboard.forms.account import BusinessInfoForm, AccountForm


def _merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAll(request):

    user_data = UserExtraSeller.objects.filter(user=request.user).first()

    if not user_data:
        _create_user_extraseller(request.user)

    data = _get_user_data(user=request.user)

    return JsonResponse({'account': data})


def _get_user_data(user, add_saldo=True):
    userextra_data = UserExtra.objects.filter(user=user).first()

    bank = UserExtraSeller.objects.filter(user=user).first()

    if userextra_data.avatar == 'ticketshop/images/default_avatar.png':
        avatar = settings.HOSTNAME + static(userextra_data.avatar)
    else:
        # media/images/upload/images/user/_aaa.jpg
        avatar = userextra_data.avatar.url
    # meh = _('test yay')
    data = {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'avatar': avatar,

        'coc_number': bank.kvk_number,
        'tax_number': bank.btw_nr,
        # de plaats van de business
        'place': bank.factuur_adress,
        'account_number': bank.rekening_number,
        'account_owner': bank.rekening_houder,

        'postal_code': bank.postal_code,
        'house_number': bank.house_number,
        'house_number_addition': bank.house_number_addition,
        'company_name': bank.company_name,
        'big': bank.big
    }
    if add_saldo:
        data['saldo'] = _get_total_saldo(user=user)

    return data


def _get_total_saldo(user):
    events = Event.objects.filter(
        eventorganiser__user__pk=user.pk,
        removed=False
    )

    total_payout = EventPayments.objects.filter(Q(event__in=events) | Q(user=user), approved=True).aggregate(Sum('amount'))

    if not total_payout['amount__sum']:
        total_payout = 0
    else:
        total_payout = total_payout['amount__sum']

    tickets = Ticket.objects.filter(event_id__in=events)
    total_price = 0

    # loop over all the tickets
    for ticket in tickets:
        sold_tickets = SoldTicket.objects.filter(
            ticket_type=ticket, order_nr__order_paid=True, is_subticket=False)

        # holds prices and amount of that price
        ticket_price_types = stats_define_price(sold_tickets, ticket)

        for ticket_price_type in ticket_price_types:
            price = ticket_price_type['price']
            amount = ticket_price_type['amount']
            total_price += round(amount * float(price), 2)

    return round(float(total_price) - float(total_payout), 2)


def stats_define_price(sold_tickets, ticket):
    ticket_price_types = []

    for sold_ticket in sold_tickets:

        price = sold_ticket.price
        # als de verkochte ticket geen prijs heeft: (alleen voor dingen van het verleden)
        if sold_ticket.price == 0:
            price = float(ticket.price) / 100

        found = False
        for t in ticket_price_types:
            if t['price'] == price:
                t['amount'] += 1
                found = True
                break

        if not found:
            ticket_price_types.append({
                'price': price,
                'amount': 1
            })

    return ticket_price_types


def _create_user_extraseller(user):
    return UserExtraSeller(user=user).save()


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user

    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    check = user.check_password(data.get('old', ''))
    success = False
    error = ''
    if not check:
        error = 'Huidig wachtwoord is incorrect'
    elif data.get('new') != data.get('new_check'):
        error = 'De velden komen niet overeen'
    else:
        user.set_password(data.get('new'))
        user.save()
        success = True

    return JsonResponse({'success':success, 'error': error})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update(request):

    if request.POST:
        business_form = BusinessInfoForm(request.POST)
        profile_object = UserExtra.objects.filter(user=request.user).first()
        profile_form = AccountForm(data=request.POST, files=request.FILES, instance=profile_object)

        if business_form.is_valid() and profile_form.is_valid():

            form_data = business_form.cleaned_data

            bank = UserExtraSeller.objects.filter(user=request.user).first()

            bank.kvk_number = form_data['coc_number']
            bank.btw_nr = form_data['tax_number']
            bank.factuur_adress = form_data['place']
            bank.rekening_houder = form_data['account_owner']
            bank.rekening_number = form_data['account_number']
            bank.postal_code = form_data['postal_code']
            bank.house_number = form_data['house_number']
            bank.house_number_addition = form_data['house_number_addition']
            bank.company_name = form_data['company_name']
            bank.big = form_data['big']
            bank.save()

            profile_form.save()

        else:

            return JsonResponse({'aa': 'error'})

    data = _get_user_data(user=request.user, add_saldo=False)

    return JsonResponse({'account': data, 'success': True})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def request_payout(request):

    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    amount = data.get('amount', '0')

    # amount check
    if float(amount) > float(_get_total_saldo(user=request.user)):
        return JsonResponse({'success': True})

    EventPayments(
        amount=amount,
        payout_date=datetime.datetime.now(),
        description='Payout request by user',
        approved=False,
        user=request.user
    ).save()

    email_message = 'user: ' + request.user.username + ' \n'
    email_message += 'amount: ' + str(amount) + ' \n'

    msg = EmailMessage('Payout requested from ' + request.user.username, email_message,
                       'noreply@yourtickets.nl', ['info@yourtickets.nl', 'almerelc@gmail.com'])
    msg.send()

    return JsonResponse({'success': True})


def logout(request):
    lgout(request)
    return JsonResponse({'success': True})
