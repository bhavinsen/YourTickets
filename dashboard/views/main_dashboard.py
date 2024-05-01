from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from dashboard.common.helpers import get_username
from ticketshop.models import (
    Event, EventOrganiser,
    TicketShopCustom,
    SharedEvents
)
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from django.http import JsonResponse


@login_required(login_url='login')
def index(request):
    querysetf = EventOrganiser.objects.filter(user=request.user).order_by('-pk')
    resultlist = []
    cshop = []
    for item in querysetf:
        resultlist.append(item.event.id)
    queryset = Event.objects.filter(pk__in=resultlist).order_by('-pk')

    for item in queryset:
        cshopObj = TicketShopCustom.objects.filter(event_id=item.id).first()

        if cshopObj:
            if cshopObj.header_img:
                cshop.append(cshopObj.header_img.url)
            else:
                cshop.append("")

    if queryset.count() > 0:
        url = queryset.first()

       # return redirect('/dashboard/' + str(url.id) + '/statistics')
        return redirect("dashboard_statistics", event_id = url.id)

    return render(request, 'dash/home.html', {
        'event_list': queryset,
        'cshop': cshop,
        'userd': request.user,
        'username_full': get_username(request),
        'shared_events':  SharedEvents.objects.filter(user=request.user).select_related('event')
    })


@login_required(login_url='login')
def gettoken(request):
    token, _ = Token.objects.get_or_create(user=request.user)
    return JsonResponse({'token': token.key})
