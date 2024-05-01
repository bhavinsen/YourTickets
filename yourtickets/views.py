import hashlib
import os
import uuid
import json

from django.http import HttpResponseNotFound
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import (
    redirect,
    render,
)
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db.models.query_utils import Q
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import abspath, dirname
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic import (
    FormView
)
from django.http import JsonResponse

from yourtickets.common.mail import create_mail, send_template_mail
from ticketshop.models import (
    UserExtra,
    accessRequests,
    DynamicUrl,
    Event,
    Order,
    Multiticketshop,
    TempSharedEvents,
    SharedEvents,
    SoldTicket,
    PageViews
)
from yourtickets.common import utils, cart
from yourtickets.common.ticket import generate_pdf_for_ticket, generate_pdf_for_order
from yourtickets.settings import DEFAULT_FROM_EMAIL
from ticketshop.forms import PasswordResetRequestForm, SetPasswordForm
from django.urls import reverse
from yourtickets.common import shop
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required

@csrf_exempt
def track(request):
    # if event exists with id
    try:
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
    except:
        return JsonResponse({'ok': 'okk'})

    user_uuid = data.get('uuid')
    event_id = data.get('event_id', '')
    url = data.get('url', '')
    if user_uuid == '':
        user_uuid = uuid.uuid4()
    # quick hack
    if len(event_id) > 10:
        event_id = ''
    if len(url) == 0:
        return JsonResponse({'ok': 'okk'})

    # if no uuid given create a new one and return it
    PageViews(uuid=user_uuid, event_id=event_id, url=url, ip='').save()
    return JsonResponse({'ok':'ok', 'uuid':user_uuid})


# test function for testing iframe
def iframe(request, event_id):

    event = Event.objects.filter(pk=event_id)

    # this is the iframe server where to serve the iframe from
    # this whole function will be deleted in the future
    if settings.HOSTNAME == 'https://yourtickets.nl':
        server = 'yourtickets.nl'
    elif settings.HOSTNAME == 'http://34.252.137.93':
        server = '34.252.137.93'
    else:
        server = '127.0.0.1:8000'

    # server = '127.0.0.1:8000'


    if len(event) == 0:
        return JsonResponse({'error': 'geen event gevonden met id '+event_id})
    else:
        event = event[0]

    event_url_str = event.event_url
    if event_url_str == "":
        event_url_str = event.title
    event_url = event_url_str

    return render(request, 'iframe.html', {
        'event': event,
        'event_url': event_url,
        'server': server
    })


def iframe_redirect(request):

    if 'payment_data' not in request.session:
        return JsonResponse({'error': 'no order found'})

    payment_data = request.session['payment_data']

    event = Event.objects.get(pk=payment_data['event_id'])
    order = Order.objects.get(pk=payment_data['order_id'])

    payment = shop.payment_custom(
        payment_data['price'],
        payment_data['title'],
        event,
        payment_data['order_id']
    )

    # request.session['payment_data'] = {
    #     'price': order_price_with_service_costs,
    #     'title': event.title + ", Order nr: " + str(order.id),
    #     'event_id': event.pk,
    #     'order_id': order.id
    # }

    # get the order and save order.mollie_id = payment['id']
    order.mollie_id = payment['id']
    order.save()

    request.session['payment_url'] = payment.checkout_url

    if request.session.get('comes_from_iframe', False):
        return redirect(payment.checkout_url)
    else:
        return JsonResponse({'error': 'not coming from iframe'})

def login_func(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:

                login(request, user)
                Token.objects.get_or_create(user=user)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

import datetime

# @login_required
def profiel(request):

    next = request.GET.get('next','')

    if request.method == 'POST':
        # next = request.POST.get('next','')

        birth_date = datetime.datetime.strptime(request.POST.get('birth_date', ''), '%d-%m-%Y').strftime('%Y-%m-%d')
        postcode = request.POST.get('postcode', '')
        gender = request.POST.get('gender', 'M')
        if birth_date != '' and postcode != '':
            userex = UserExtra(user=request.user, birth_date=birth_date, adress=postcode, sex=gender)
            userex.save()
            if next:
                return redirect(next)
            else:
                return redirect(reverse('dashboard_index'))
        else:
            return render(request, 'yourtickets/profile.html', {
                'error': 'Je hebt niet alles ingevuld'
            })
    else:
        return render(request, 'yourtickets/profile.html', {'next':next})




def contact(request):
    if request.POST:
        text = request.POST['text_question']
        name = request.POST['name']
        email = request.POST['email']

        send_mail(
            'Contact formulier',
            'Contact formulier in ingevuld met tekst: \n' + text + '\nNaam:\n' + name + '\nEmail:\n' + email,
            DEFAULT_FROM_EMAIL,
            ['support@yourtickets.nl'],
            fail_silently=False,
        )

        return render(request, 'yourtickets/contact.html', {
            'error': 'Verzonden'})
    else:
        return render(request, 'yourtickets/contact.html', {
        })

def lost_tickets(request):
    tickets = []
    searched = False
    description = ''
    if request.POST:
        description = request.POST.get('description', '')
        searched = True

        order = Order.objects.filter(order_paid=True, uid=description)

        tickets = SoldTicket.objects.filter(order_nr=order,order_nr__order_paid=True).select_related('event', 'ticket_type')

    return render(request, 'yourtickets/lostticket.html', {
        'tickets':tickets,
        'searched': searched,
        'description': description
    })

def download_ticket(request, description, ticket_id):
    if not Order.objects.filter(order_paid=True, uid=description).exists():
        return

    ticket = SoldTicket.objects.filter(pk=ticket_id).first()

    file_path = generate_pdf_for_ticket(ticket, download=True)

    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response


def download_all(request, description):
    if not Order.objects.filter(order_paid=True, uid=description).exists():
        return



    file_path = generate_pdf_for_order(Order.objects.filter(order_paid=True, uid=description).first(), download=True)

    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response


def home_beta(request):
    send = False
    if request.POST:
        email = request.POST['email']
        req = accessRequests(email=email)
        req.save()
        send = True

    return render(request, 'betabedankt.html', {
        'send': send
    })


def login_req(request):
    # logout(request)
    if request.POST:

        username = request.POST['username'].lower()
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if request.user.is_superuser:
            user = User.objects.filter(username=username).first()


            if user:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard_index'))

        if user is not None:
            if user.is_active:
                login(request, user)

                # return HttpResponseRedirect(request.session.get('ref', reverse('dashboard_index')))
                return HttpResponseRedirect(reverse('dashboard_index'))
            else:
                return render(request,'yourtickets/login.html', {
                    'error': utils.getWord(utils.getCurrentLanguage(request), "login-error-wrong", request)
                })
        else:
            return render(request, 'yourtickets/login.html', {
                'error': utils.getWord(utils.getCurrentLanguage(request), "login-error-wrong", request)
            })

    request.session['ref'] = request.META.get('HTTP_REFERER')
    return render(request, 'yourtickets/login.html', {
    })

def logout_req(request):

    session_cart = cart.Cart(request)
    cart_session = session_cart.storage

    logout(request)

    request.session['cart'] = cart_session

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

from yourtickets.forms import RegisterForm

def register_req(request):
    # logout(request)

    error = ''

    activation_mail_send = False
    email = ''

    if request.POST:

        register_form = RegisterForm(request.POST)

        existing_user = User.objects.filter(username__iexact=request.POST['username'])

        # form not valid
        if not register_form.is_valid():

            error = utils.getWord(utils.getCurrentLanguage(request), "register-error-emptyfields", request)

        # user exists allready
        elif existing_user:

            error = utils.getWord(utils.getCurrentLanguage(request), "register-error-userexists", request)

        # if user form is filled in correctly and user does not exists
        elif register_form.is_valid() and not existing_user:

            form_data = register_form.cleaned_data

            user = User.objects.create_user(
                form_data['username'],
                form_data['username'],
                form_data['password'],
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                is_active=False
            )

            user.save()
            token = hashlib.md5((settings.ACTIVATION_SALT+form_data['username']).encode('utf-8')).hexdigest()

            userEx = UserExtra(
                user=user, birth_date='1970-01-01',
                adress='1111AA', sex='M', is_organizer=True, is_visitor=False,
                activate_token=token, terms_agreed=True

            )

            userEx.save()

            if TempSharedEvents.objects.filter(user_email=user.username).exists():
                temp_objs = TempSharedEvents.objects.filter(user_email=user.username)
                for temp_obj in temp_objs:
                    SharedEvents.objects.create(event=temp_obj.event, user=user)
                    temp_obj.delete()

            # send the activation mail
            url = settings.HOSTNAME + reverse('account_activate', kwargs={'token': token})

            send_template_mail('emails/email_verification.html',{
                'title': 'Verifieer jouw e-mailadres',
                'button_link': url,
                'current_year': datetime.datetime.now().year
            }, 'Verifieer jouw e-mailadres', form_data['username'])

            activation_mail_send = True
            email = form_data['username']

            user = authenticate(username=form_data['username'], password=form_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('dashboard_index'))
    else:
        register_form = RegisterForm()

    return render(request, 'yourtickets/register.html', {
        'activation_mail_send': activation_mail_send,
        'email': email,
        'register_form': register_form,
        'error': error
    })


def account_activate(request, token):
    userextra = UserExtra.objects.filter(activate_token=token).first()

    if not userextra:
        return HttpResponseRedirect(reverse('login', kwargs={}))

    user = userextra.user
    user.is_active = True
    user.save()

    userextra.activate_token = ''
    userextra.save()

    return HttpResponseRedirect(reverse('login', kwargs={}))


def usernameExists(request, user):
    try:
        user_exists = User.objects.get(username=user)
        return HttpResponse("1")
    except User.DoesNotExist:
        return HttpResponse('0')

#@login_required
def custom_event_url(request, event_name):
    objects = DynamicUrl.objects.filter(url_name=event_name, enabled=True)

    if len(objects) == 0:
        return handler404(request)
    else:
        object = objects[0]

        if object.type == DynamicUrl.EVENT:
            event = Event.objects.filter(pk=object.event_id).first()
            return HttpResponseRedirect(
                reverse('buy_ticket', kwargs={'event_id': event.id, 'event_name': event.event_url}))
        elif object.type == DynamicUrl.MULTITICKETSHOP:

            shopp = Multiticketshop.objects.filter(pk=object.multiticketshop_id).first()
            return HttpResponseRedirect(
                reverse('multiticketshop', kwargs={'multiticketshop_id': shopp.id}))

        return handler404(request)




def customUrlRoomservice(request, name):

    if name == 'bitterorbetter':
        return HttpResponseRedirect('/ticketshop/105/Bitter_or_Better/')
    elif name == 'baller':
        # https://yourtickets.nl/nl/ticketshop/127/BALLER/
        return HttpResponseRedirect('/ticketshop/127/BALLER/')

    elif name == 'cakebash':
        return HttpResponseRedirect('/ticketshop/130/Cake-Bash/')
    elif name == 'blackfriday':
        return HttpResponseRedirect('/ticketshop/139/Black_Friday/')
    elif name == 'blaque':
        return HttpResponseRedirect('/ticketshop/132/Blaque/')
    elif name == 'bizarr':
        return HttpResponseRedirect('/ticketshop/135/Bizarr/')
    elif name == 'runtown':
        return HttpResponseRedirect('/ticketshop/138/Runtown_-_Mad_over_you/')
    elif name == 'pleasure':
        return HttpResponseRedirect('/ticketshop/136/PLEASURE/')
    elif name == 'surifiesta':
        return HttpResponseRedirect('/ticketshop/141/Suri_Fiesta/')
    elif name == 'stoutennieuw':
        return HttpResponseRedirect('/ticketshop/142/Stout_&_Nieuw/')
    elif name == 'streetview':
        return HttpResponseRedirect('/ticketshop/123/Streetview/')
    elif name == 'gyalabubble':
        return HttpResponseRedirect('/ticketshop/153/Gyal_A_Bubble/')
    elif name == 'seduction':
        return HttpResponseRedirect('/ticketshop/152/seduction/')


class ResetPasswordRequestView(FormView):
    template_name = "yourtickets/forgot_password.html"    #code for template is given below the view's code
    success_url = '/login'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                data= form.cleaned_data["email_or_username"].lower()
            if self.validate_email_address(data) is True:                 #uses the method written above
                '''
                If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
                '''
                # import pdb;
                # pdb.set_trace()
                associated_users= User.objects.filter(Q(email=data)|Q(username=data))
                if associated_users.exists():
                    for user in associated_users:

                        c = {
                            'email': user.email,
                            'domain': 'yourtickets.nl',
                            'site_name': 'Yourtickets',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }

                        subject = "Wachtwoord vergeten!"
                        email_template_name='emails/password_reset_email_html.html'
                        email = loader.render_to_string(email_template_name, c)

                        html_part = MIMEMultipart(_subtype='related')

                        body = MIMEText(email.encode('utf-8'), _subtype='html', _charset='utf-8')
                        html_part.attach(body)

                        img_data = open(settings.EMAIL_MEDIA_IMAGE_DIR + 'facebook.png', 'rb').read()
                        img = MIMEImage(img_data, 'png')
                        img.add_header('Content-Id', '<fb>')  # angle brackets are important
                        img.add_header("Content-Disposition", "inline", filename="fb") # David Hess recommended this edit
                        html_part.attach(img)

                        img_data = open(settings.EMAIL_MEDIA_IMAGE_DIR + 'twitter.png', 'rb').read()
                        img = MIMEImage(img_data, 'png')
                        img.add_header('Content-Id', '<twitter>')  # angle brackets are important
                        img.add_header("Content-Disposition", "inline", filename="twitter") # David Hess recommended this edit
                        html_part.attach(img)

                        img_data = open(settings.EMAIL_MEDIA_IMAGE_DIR+'instagram.png', 'rb').read()
                        img = MIMEImage(img_data, 'png')
                        img.add_header('Content-Id', '<insta>')  # angle brackets are important
                        img.add_header("Content-Disposition", "inline", filename="insta") # David Hess recommended this edit
                        html_part.attach(img)

                        img_data = open(settings.EMAIL_MEDIA_IMAGE_DIR+'website.png', 'rb').read()
                        img = MIMEImage(img_data, 'png')
                        img.add_header('Content-Id', '<website>')  # angle brackets are important
                        img.add_header("Content-Disposition", "inline", filename="website") # David Hess recommended this edit
                        html_part.attach(img)

                        # dit gaf een error
                        # msg = EmailMessage(subject, None, DEFAULT_FROM_EMAIL , [user.email])
                        msg = EmailMessage(
                            subject=subject,
                            from_email=DEFAULT_FROM_EMAIL,
                            to=[user.email],
                        )
                        msg.attach(html_part)
                        msg.send()

                    result = self.form_valid(form)
                    #messages.success(request, 'Een email is verstuurd naar ' + data +".")
                    return result
                result = self.form_invalid(form)
                messages.error(request, 'Emailadres is onbekend')
                return result
            else:
                '''
                If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
                '''
                associated_users= User.objects.filter(username=data)
                if associated_users.exists():
                    for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'Yourtickets',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }
                        subject_template_name='registration/password_reset_subject.txt'
                        email_template_name='emails/password_reset_email_html.html'
                        subject = loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        # subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)

                    result = self.form_valid(form)
                    messages.success(request, 'Email is verstuurd naar ' + data +"'s email address.")
                    return result
                result = self.form_invalid(form)
                messages.error(request, 'Deze gebruiker bestaat niet.')
                return result
            messages.error(request, 'Verkeerde input')
        except Exception as e:

            print(e)
        return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
    template_name = "account/test_template.html"
    success_url = '/login'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():

                new_password= form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Wachtwoord veranderen is gelukt.')
                return self.form_valid(form)
            else:
                #messages.error(request, 'Wachtwoord veranderen is mislukt.')
                return self.form_invalid(form)
        else:
            messages.error(request,'Wachtwoord veranderen link is niet meer geldig.')
            return self.form_invalid(form)

def handler404(request, exception=''):
    # response = render(request, 'app/404.html', {})
    # response.status_code = 404
    print('---------ERROR 404')
    print(request.build_absolute_uri())
    try:
        print('user: ' + request.user.username)
    except Exception as e:
        pass
    print(request)
    print('---------END ERROR')
    #return HttpResponseNotFound(request, 'app/404.html')

    return redirect('error_page', error_id=404)

def handler500(request):
    # response = render(request, 'app/500.html', {})
    # response.status_code = 500
    print('---------ERROR 500')
    print(request.build_absolute_uri())
    try:
        print('user: ' + request.user.username)
    except Exception as e:
        pass
    print(request)
    print('---------END ERROR')
    #return response
    return redirect('error_page', error_id=500)


def error_page(request,error_id):

    if error_id == 404:
        response = render(request, 'app/404.html', {})
        response.status_code = 404
    elif error_id == 500:
        response = render(request, 'app/500.html', {})
        response.status_code = 500
    else:
        response = render(request, 'app/404.html', {})
        response.status_code = 404

    response.status_code = 200
    return  response