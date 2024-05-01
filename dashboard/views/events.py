import json
import re
import time
from django.shortcuts import render
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponseRedirect

from ticketshop.models import (
    Event, EventOrganiser,
    Ticket, LineUp,
    TicketShopCustom,
    Languages)
from django.shortcuts import redirect

from django.template import RequestContext
from django.conf import settings
from django.urls import reverse
from yourtickets.common import utils, shop
from django.core.mail import EmailMessage
from dashboard.views.forms import TicketShopCustomForm
from youradmin.common.decorators import is_event_from_user
from django.contrib.auth.decorators import login_required


@csrf_exempt
def event_new(request):

    if request.user.is_authenticated:
        c = {}
        c.update(csrf(request))

        if request.method == 'POST':
            start_date_var = request.POST.get('start-date', '2000-01-01') + ' ' + request.POST.get('start-time', '00:00')
            end_date_var = request.POST.get('end-date', '2000-01-01') + ' ' + request.POST.get('end-time', '00:00')
            if start_date_var == " " or end_date_var == " ":
                return render(request, 'app/step_one.html', {'error': "Niet alles was correct ingevuld." }, context_instance=RequestContext(request))
            event_url = request.POST.get('eventurl', '').replace("/", "")
            event_url = event_url.replace(" ", "_")
            eventObj = Event(title=request.POST.get('title', 'Geen titel'),
                location=request.POST.get('locatie', 'Geen locatie opgegeven'),
                description=request.POST.get('description', 'Geen beschrijving'),
                start_date=start_date_var,
                end_date=end_date_var,
                service_cost='100', event_public=True, unique_tickets=False,
                event_url=event_url)
            eventObj.save()

            form = TicketShopCustomForm(data={
                'event_id': eventObj.pk,
                'primary_color': request.POST.get('primColor', '#000000'),
                'secondary_color': request.POST.get('secColor', '#FFFFFF'),
                'header_img': request.FILES.get('image_header'),
                'bg_img': request.FILES.get('image_backgr')
            }, files={
                'header_img': request.FILES.get('image_header'),
                'bg_img': request.FILES.get('image_backgr'),
            })

            if form.is_valid():
                form.save()

            else:
                start_date = time.strftime("%Y-%m-%d")
                start_time = "00:00"
                return render(request, 'dash/event/create/step_one.html', {
                    'lc': utils.getCurrentLanguage(request),
                    'langs': getLanguages(request),
                    'start_date': start_date,
                    'start_time': start_time
                })
                # print(json.loads(form.errors.as_json()))
                # print('================================= not valid')

            # ticketShopCustom = TicketShopCustom(event_id=eventObj,
            #     primary_color=request.POST.get('primColor', '#000000'),
            #     secondary_color=request.POST.get('secColor', '#FFFFFF'),
            #     header_img=request.FILES.get('image_header'),
            #     bg_img=request.FILES.get('image_backgr'))
            # ticketShopCustom.save()

            eventOrg = EventOrganiser(event=eventObj, user=request.user,
                admin_rights=2)
            eventOrg.save()

            artistsNames = request.POST.getlist('artiestenLijstNaam[]')
            #artistsUrls = request.POST.getlist('artiestenLijstUrl[]')
            x = 0
            for item in artistsNames:
                #lineUpObj = LineUp(event_id=eventObj, artist=item, url=artistsUrls[x])
                lineUpObj = LineUp(event_id=eventObj, artist=item, url="")
                lineUpObj.save()
                x += 1

            ticketNames = request.POST.getlist('ticketNaam[]')
            ticketPrijs = request.POST.getlist('ticketPrijs[]')
            ticketAantal = request.POST.getlist('ticketAantal[]')
            ticketStart = request.POST.getlist('ticketStart[]')
            ticketEnd = request.POST.getlist('ticketEind[]')
            ticketMax = request.POST.getlist('ticketMax[]')
            person_amount = request.POST.getlist('person_amount[]')

            x = 0
            for item in ticketNames:
                ticket_price_integer = int(re.sub("[^0-9]", "", ticketPrijs[x]) )
                #ticket_price = float(ticket_price_integer ) / 100
                #ticket_service_costs_gross = shop.get_service_cost(ticket_price, 1, 0)
                #ticket_service_costs = shop.get_service_cost(ticket_price, 1, eventObj.service_cost_discount_cents)
                #ticket_service_costs_discount = ticket_service_costs_gross - ticket_service_costs
                TicketObj = Ticket(
                    event=eventObj,
                    name=item,
                    description='',
                    #price=re.sub("[^0-9]", "", ticketPrijs[x]),
                    price=ticket_price_integer,
                    quantity=ticketAantal[x],
                    start_date=ticketStart[x],
                    end_date=ticketEnd[x],
                    max_sold=ticketMax[x],
                    person_amount= person_amount[x] #,
                    #service_costs_gross=ticket_service_costs_gross * float(ticketAantal[x]),
                    #service_costs=ticket_service_costs * float(ticketAantal[x]),
                    #service_costs_discount=ticket_service_costs_discount * float(ticketAantal[x]),
                    #total = ticket_price * float(ticketAantal[x]),
                    #total_person_amount = int(person_amount[x]) * int(ticketAantal[x])
                )
                TicketObj.save()
                TicketObj.update_totals()
                x += 1
            eventObj.update_tickets_totals()

            url = settings.HOSTNAME+reverse('buy_ticket', kwargs={'event_id': eventObj.id, 'event_name': eventObj.event_url})
            # get_current_site(request).domain + "/ticketshop/" + str(eventObj.id) + "/" + eventObj.event_url

            email_message = 'event name: ' + eventObj.title + ' \n'
            email_message += 'organisator email: ' + request.user.email + ' \n'
            email_message += 'event datum: ' + eventObj.start_date + ' \n'
            email_message += 'https://yourtickets.nl/youradmin'

            msg = EmailMessage('Event created ' + eventObj.title + ' id:'+ str(eventObj.pk), email_message, 'noreply@yourtickets.nl', ['info@yourtickets.nl', 'almerelc@gmail.com'])
            msg.send()

            return HttpResponseRedirect(reverse('event_new_completed', kwargs={'event_id': eventObj.pk}))

        else:
            start_date = time.strftime("%Y-%m-%d")
            # start_date = datetime.datetime.strftime("%Y-%m-%d")
            start_time = "00:00"
            return render(request, 'dash/event/create/step_one.html', {
                'lc': utils.getCurrentLanguage(request),
                'langs': getLanguages(request),
                'start_date': start_date,
                'start_time': start_time
            })

    else:
        return redirect(reverse('login'))

@is_event_from_user(login_url='login')
@login_required(login_url='login')
def event_new_completed(request, event_id):

    event = Event.objects.filter(pk=event_id).first()
    url = settings.HOSTNAME + reverse('buy_ticket', kwargs={'event_id': event.id, 'event_name': event.event_url})

    return render(request, 'app/event_created.html', {
        'lc': utils.getCurrentLanguage(request),
        'langs': getLanguages(request), 'url': url})

def getLanguages(request):
    language_list = []

    languages = Languages.objects.filter()
    for lg in languages:
        language_list.append([lg.language_code,lg.language_name])
    return language_list
