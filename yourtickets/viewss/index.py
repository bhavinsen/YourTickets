

import hashlib

from django.contrib.auth.decorators import (
    login_required
)
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import (
    # render_to_response,
    redirect,
    render,
)
from django.urls import reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http.response import HttpResponseRedirect
from ticketshop.models import (
    PreReg
)

def index(request):

    # from yourtickets.common.ticket import send_single_ticket_mail, generate_pdf_for_ticket
    # from ticketshop.models import SoldTicket
    # sold_ticket = SoldTicket.objects.get(id=1043)
    # print(sold_ticket)
    # generate_pdf_for_ticket(ticket=sold_ticket)
    
    # m = Image.open(requests.get('', stream=True).raw)
    # img_data = open('https://cdn.yourtickets.nl/images/event/Almeres_finest_days_gym_tickets.jpg', 'rb').read()
    # a = AbstractApplication()
    return render(request, 'yourtickets2/main.html', {})

def pre_reg(request):
    post_and_error = False
    first_name = None
    last_name = None
    email = None
    phone_number = None
    country = None
    notify_me = None
    if request.POST:

        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        phone_number = request.POST.get('phone_number', None)
        country = request.POST.get('country', None)
        notify_me = True if request.POST.get('notify_me', False) else False
        if first_name and email and phone_number and country:
            try:
                validate_email(email)
                prereg = PreReg(
                    first_name=first_name, 
                    last_name=last_name, 
                    email=email, 
                    phone_number=phone_number, 
                    country=country, 
                    notify_me=notify_me
                )
                prereg.save()
                return HttpResponseRedirect(reverse('pre_reg_succes', kwargs={}))

            except ValidationError as e:
                post_and_error = True
        else:
            post_and_error = True
        
        
    return render(request, 'yourtickets/pre_reg.html', {
        'post_and_error': post_and_error,
        'first_name':first_name, 
        'last_name':last_name,
        'email':email,
        'phone_number':phone_number,
        'country':country,
        'notify_me':notify_me
    })

def pre_reg_succes(request):
    return render(request, 'yourtickets/pre_reg_succes.html', {})