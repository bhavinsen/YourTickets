import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from dashboard.views.forms import TicketShopCustomForm
from youradmin.common.decorators import is_event_from_user
from dashboard.common.base_vars import base_vars
from ticketshop.models import Event, TicketShopCustom


@is_event_from_user(login_url='login')
@login_required(login_url='login')
def index(request, event_id):

    if request.POST:
        event = Event.objects.filter(pk=event_id).first()

        data = request.POST.copy()
        data['event_id'] = event.pk
        data['primary_color'] = data['primColor']
        data['secondary_color'] = data['secColor']

        print(request.FILES)
        print('-------')
        print(data)

        form = TicketShopCustomForm(data, files=request.FILES, instance=TicketShopCustom.objects.get(event_id=event))

        if form.is_valid():
            form.save()
        else:


            print(json.loads(form.errors.as_json()))
            # print('================================= not valid')

        # tsc = TicketShopCustom.objects.get(event_id=event)
        # tsc.primary_color = request.POST['primColor']
        # tsc.secondary_color = request.POST['secColor']
        # if (request.FILES.get('header_img')):
        #     tsc.header_img = request.FILES.get('header_img')
        # if (request.FILES.get('bg_img')):
        #     tsc.bg_img = request.FILES.get('bg_img')
        # tsc.save()

    return render(request, 'dash/event/edit/ticketshop.html', base_vars(request, event_id, {
        'curl': 'ticketshop'
    }))
