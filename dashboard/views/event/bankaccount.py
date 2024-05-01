from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from youradmin.common.decorators import is_event_from_user
from dashboard.common.base_vars import base_vars
from ticketshop.models import Event, UserExtraSeller


@is_event_from_user(login_url='login')
@login_required(login_url='login')
def index(request, event_id):

    event = Event.objects.filter(pk=event_id).first()
    bank = UserExtraSeller.objects.filter(event_id=event.id).first()

    if request.POST:
        kvk = request.POST['kvk']
        btw = request.POST['btw']
        fact = request.POST['fact_adres']
        rek_h = request.POST['rek_houder']
        rek_nr = request.POST['rek_nr']
        if not bank:
            bank = UserExtraSeller(event_id=event, kvk_number=kvk, btw_nr=btw, factuur_adress=fact,
                                   rekening_houder=rek_h, rekening_number=rek_nr)
        else:
            bank.kvk_number = kvk
            bank.btw_nr = btw
            bank.factuur_adress = fact
            bank.rekening_houder = rek_h
            bank.rekening_number = rek_nr
        bank.save()

    return render(request, 'dash/event/edit/bank.html', base_vars(request, event_id, {
        'bank': bank,
        'curl': 'bank'
    }))
