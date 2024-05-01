# -*- coding: utf8 -*-
import os
from PIL import Image
import requests
from urllib.request import urlopen
from urllib.parse import urljoin



from fpdf import FPDF
# from fpdf import set_global

# set_global('FPDF_FONT_DIR', os.path.join(os.path.dirname(__file__),'font'))



import struct
from django.utils import timezone
from django.template import loader
import pyqrcode
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from os.path import abspath, dirname
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.templatetags.static import static

from yourtickets.common import utils
from ticketshop.models import (
    Event,
    SoldTicket,
    TicketShopCustom
)


def send_ticket_mail(order, language_param = 'nl', emailvar=None, base_url=None):

    from yourtickets.common.log import writeOrderLog
    from ticketshop.models import Orderlog
    

    tickets = SoldTicket.objects.filter(order_nr=order.id)
    # shop_url = request.META['HTTP_HOST'] + '/ticketshop/buy/' + str(order.id) + '/'
    shop_url = settings.HOSTNAME + reverse('buy_ticket_mollie', kwargs={'order_id': order.id})

    tick = tickets.first()
    event = Event.objects.get(pk=tick.event.id)
    cshop = TicketShopCustom.objects.filter(event_id=event.id).first()

    language_from_order = order.ordered_in_language

    # ticket_gens = []
    # for ticket in tickets:
    #     random_number = ticket.ticket_gen_id
    #     ticket_gens.append([settings.HOSTNAME + '/media/tickets/html/ticket-' + str(random_number) + '.html'])

    c = {
        'shop_url': shop_url,
        'event_name': event.title,
        # 'ticket_links': ticket_gens
    }

    if language_from_order == 'unknown':
        language = 'NL'
    else:
        language = language_from_order

    if language == 'FR':
        c['text1'] = 'chargez votre/vos billet(s) pour ' + event.title +'!'
        c['text2'] = 'Vous recevez maintenant votre/vos billet(s) pour '+ event.title +'!'
    elif language == 'EN':
        c['text1'] = 'Download your ticket(s) for ' + event.title + '!'
        c['text2'] = 'Your purchase is added to this email as attachment. Any questions? Mail to: support@yourtickets.nl'
    else:
        c['text1'] = 'Download nu jouw ticket(s) voor '+event.title+'!'
        c['text2'] = 'Jouw aankoop is als bijlage toegevoegd aan deze mail. Heb je een vraag? Mail naar: tickets@yourtickets.nl'

    subject = utils.getWord(language, "email-buytickets-title")

    email_template_name = 'emails/' + language.upper() + '/buytickets.html'
    email = loader.render_to_string(email_template_name, c)
    text = email
    from_rec = "noreply@yourtickets.nl"

    html_part = MIMEMultipart(_subtype='related')

    body = MIMEText(text.encode('utf-8'), _subtype='html', _charset='utf-8')
    html_part.attach(body)

    # img_data = Image.open(requests.get(cshop.header_img.url, stream=True).raw).  # open(cshop.header_img.url, 'rb').read()
    relative_image_url = cshop.header_img.url
    image_url = urljoin(base_url, relative_image_url)
    img_data = urlopen(image_url).read()
    img = MIMEImage(img_data, 'png')
    img.add_header('Content-Id', '<logo>')  # angle brackets are important
    img.add_header("Content-Disposition", "inline", filename="logo") # David Hess recommended this edit
    html_part.attach(img)

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

    working_dir = settings.TEMP_TICKET_CREATION_DIR
    attachments_per_mail = dict()
    for ticket in tickets:
        if emailvar is not None and emailvar not in attachments_per_mail:
            attachments_per_mail[emailvar] = list()
        elif not ticket.email in attachments_per_mail:
            attachments_per_mail[ticket.email] = list()

        content = open(working_dir + str(ticket.ticket_gen_id) + '.pdf', 'rb').read()
        attachment = (str(ticket.ticket_gen_id) + '.pdf', content, 'application/pdf')

        email_to = ticket.email

        if emailvar is not None:
            email_to = emailvar

        attachments_per_mail[email_to].append(attachment)

    for mail in attachments_per_mail:
        attachments = attachments_per_mail[mail]

        msg = EmailMessage(
            subject=subject,
            from_email="noreply@yourtickets.nl",
            to=[mail],
            bcc=['marciano.remak@yourtickets.nl'],
            attachments=attachments
        )
        msg.attach(html_part)
        msg.send()

        writeOrderLog(order_id=order.id, type=Orderlog.TYPE_MAIL_SEND)


def send_mail_and_create_pdfs(order, base_url=None, email=None):

    language_from_order = order.ordered_in_language

    if language_from_order == 'unknown':
        language = 'nl'
    else:
        language = language_from_order


    generate_pdf_tickets_for_order(order)

    # if not order.mail_send:
    send_ticket_mail(order, language, emailvar=email, base_url=base_url)

    # cleanup temp_creation_dir
    tickets = SoldTicket.objects.filter(order_nr=order.id)
    for ticket in tickets:
        working_dir = settings.TEMP_TICKET_CREATION_DIR

        qrcode_filename = working_dir + str(ticket.ticket_gen_id) + '.png'
        pdf_filename = working_dir + str(ticket.ticket_gen_id) + '.pdf'

        os.remove(qrcode_filename)
        os.remove(pdf_filename)

def send_single_ticket_mail(ticket, mail_type=''):

    # shop_url = request.META['HTTP_HOST'] + '/ticketshop/buy/' + str(order.id) + '/'
    # shop_url = settings.HOSTNAME + reverse('buy_ticket_mollie', kwargs={'order_id': order.id})

    # tick = tickets.first()
    event = Event.objects.get(pk=ticket.event.id)
    cshop = TicketShopCustom.objects.filter(event_id=event.id).first()


    header_image = settings.CUSTOM_SHOP_UPLOAD_DIR + '/yourtickets/static/yourtickets/img/header.jpg'

    if cshop:
        header_image = cshop.header_img.url

    c = {
        # 'shop_url': shop_url,
        'event_name': event.title,
        # 'ticket_links': ticket_gens
    }

    language = 'nl'

    if mail_type == 'ticket_mail_with_data':

        subject = 'Download nu jouw ticket(s) voor [Event naam]!'
        c['hi_customer'] = 'Hi '+ticket.first_name+','
        c['text1'] = 'Klik op de onderstaande button om jouw ticket(s) te downloaden!'
        c['button'] = '<a href="'++'">Download</a>'
        c['text2'] = 'Heb je een vraag? Mail naar: tickets@yourtickets.nl'

    elif mail_type == 'ticket_mail_without_data':
        subject = 'Alsjeblieft, jouw ticket(s) voor '+ event.title +'!'
        c['hi_customer'] = 'Hi '+ticket.first_name+','
        c['text1'] = 'Hierbij ontvang je jouw special guest ticket(s) voor '+event.title+'!'
        c['text2'] = 'Jouw aankoop is als bijlage toegevoegd aan deze mail. Heb je een vraag? Mail naar: tickets@yourtickets.nl'

    else:
        # old but do we need translations in this?!
        # subject = utils.getWord(language, "email-buytickets-title")
        subject = 'Alsjeblieft, jouw ticket(s) voor '+ event.title +'!'
        c['text1'] = 'Download nu jouw ticket(s) voor '+event.title+'!'
        c['text2'] = 'Jouw aankoop is als bijlage toegevoegd aan deze mail. Heb je een vraag? Mail naar: tickets@yourtickets.nl'

    email_template_name = 'emails/' + language.upper() + '/buytickets.html'
    email = loader.render_to_string(email_template_name, c)
    text = email

    html_part = MIMEMultipart(_subtype='related')

    body = MIMEText(text.encode('utf-8'), _subtype='html', _charset='utf-8')
    html_part.attach(body)

    # img_data = Image.open(requests.get(header_image, stream=True).raw)  # open(header_image, 'rb').read()
    try:
        img_data = urlopen( header_image).read()
    except : 
        img_data = open(settings.BASE_DIR + header_image, 'rb').read()
    img = MIMEImage(img_data, 'png')
    img.add_header('Content-Id', '<logo>')  # angle brackets are important
    img.add_header("Content-Disposition", "inline", filename="logo") # David Hess recommended this edit
    html_part.attach(img)

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

    working_dir = settings.TEMP_TICKET_CREATION_DIR
    attachments_per_mail = dict()

    if not ticket.email in attachments_per_mail:
        attachments_per_mail[ticket.email] = list()

    content = open(working_dir + str(ticket.ticket_gen_id) + '.pdf', 'rb').read()
    attachment = (str(ticket.ticket_gen_id) + '.pdf', content, 'application/pdf')

    email_to = ticket.email

    attachments_per_mail[email_to].append(attachment)

    for mail in attachments_per_mail:
        attachments = attachments_per_mail[mail]

        msg = EmailMessage(
            subject=subject,
            from_email="noreply@yourtickets.nl",
            to=[mail],
            bcc=['tickets@yourtickets.nl'],
          #  attachments=attachments
        )
        msg.attach(html_part)
        for attachment in attachments:
            msg.attach(*attachment)
        msg.send()


def send_mail_and_create_pdf_for_ticket(ticket, mail_type=''):
    generate_pdf_for_ticket(ticket)

    send_single_ticket_mail(ticket, mail_type)

    working_dir = settings.TEMP_TICKET_CREATION_DIR

    qrcode_filename = working_dir + str(ticket.ticket_gen_id) + '.png'
    pdf_filename = working_dir + str(ticket.ticket_gen_id) + '.pdf'
    os.remove(qrcode_filename)
    os.remove(pdf_filename)


def generate_pdf_for_ticket(ticket, download=False):

    event = Event.objects.get(pk=ticket.event.id)
    cshop = TicketShopCustom.objects.filter(event_id=event.id).first()

    start = timezone.localtime(event.start_date)
    end = timezone.localtime(event.end_date)
    event_date = start.strftime("%d %B %y | %H:%M") + " - " + end.strftime("%H:%M")
    formatted_date = start.strftime("%d %B %y")
    formatted_time = start.strftime("%H:%M")

    language = 'nl'

    working_dir = settings.TEMP_TICKET_CREATION_DIR

    qrcode_filename = working_dir + str(ticket.ticket_gen_id) + '.png'
    pdf_filename = working_dir + str(ticket.ticket_gen_id) + '.pdf'

    url = pyqrcode.create(str(ticket.ticket_gen_id))
    url.png(qrcode_filename, scale=8)

    created_pdf = PDF(language=language)

    primary_color = '#B2283A'
    # when there is no image do this
    # alltough it should have a cshop at all time
    # does images/event/header.jpg exists in settings.MEDIA_ROOT_FIX + the dir of cshop.header_img.url
    # banner_image = settings.MEDIA_ROOT_FIX + '/ticketshop/static/images/event/header.jpg'
    banner_image = settings.STATIC_URL+'images/event/header.jpg'
    if cshop:
        primary_color = cshop.primary_color
        
        banner_image = cshop.header_img.url


    created_pdf.create(
        primary_color=primary_color,
        banner_image=banner_image,  # settings.MEDIA_ROOT+'/template/banner.jpg',
        event_title=event.title,
        event_date=formatted_date,
        event_time=formatted_time,
        event_price='€ '+str(utils.currency(ticket.price)),
        event_location=event.location,
        name=ticket.first_name + " " + ticket.last_name,
        ticket_type="Gastenlijst ticket",
        qrcode=qrcode_filename
    )

    if download:
        created_pdf.output(name=pdf_filename, dest='F')
        return pdf_filename

    created_pdf.output(pdf_filename, 'F')


def generate_pdf_for_order(order, download=False):
    tickets = SoldTicket.objects.filter(order_nr=order)

    language = 'nl'

    created_pdf = PDF(language=language)

    for ticket in tickets:
        event = Event.objects.get(pk=ticket.event.id)
        cshop = TicketShopCustom.objects.filter(event_id=event.id).first()

        start = timezone.localtime(event.start_date)
        end = timezone.localtime(event.end_date)
        event_date = start.strftime("%d %B %y | %H:%M") + " - " + end.strftime("%H:%M")
        formatted_date = start.strftime("%d %B %y")
        formatted_time = start.strftime("%H:%M")


        working_dir = settings.TEMP_TICKET_CREATION_DIR

        qrcode_filename = working_dir + str(ticket.ticket_gen_id) + '.png'
        pdf_filename = working_dir + str(ticket.ticket_gen_id) + '.pdf'

        url = pyqrcode.create(str(ticket.ticket_gen_id))
        url.png(qrcode_filename, scale=8)

        created_pdf.create(
            primary_color=cshop.primary_color,
            banner_image=cshop.header_img.url, # settings.MEDIA_ROOT+'/template/banner.jpg',
            event_title=event.title,
            event_date=formatted_date,
            event_time=formatted_time,
            event_price='€ '+str(utils.currency(ticket.price)),
            event_location=event.location,
            name=ticket.first_name + " " + ticket.last_name,
            ticket_type="Gastenlijst ticket",
            qrcode=qrcode_filename
        )

    if download:
        created_pdf.output(name=pdf_filename, dest='F')
        return pdf_filename

    created_pdf.output(pdf_filename, 'F')


def generate_pdf_tickets_for_order(order):
    tickets = SoldTicket.objects.filter(order_nr=order.id)

    event = Event.objects.get(pk=tickets[0].event.id)
    cshop = TicketShopCustom.objects.filter(event_id=event.id).first()

    start = timezone.localtime(event.start_date)
    end = timezone.localtime(event.end_date)
    event_date = start.strftime("%d %B %y | %H:%M") + " - " + end.strftime("%H:%M")
    formatted_date = start.strftime("%d %B %y")
    formatted_time = start.strftime("%H:%M")

    language_from_order = order.ordered_in_language

    from yourtickets.common.log import writeOrderLog
    from ticketshop.models import Orderlog
    

    if language_from_order == 'unknown':
        language = 'nl'
    else:
        language = language_from_order

    for ticket in tickets:
        working_dir = settings.TEMP_TICKET_CREATION_DIR

        qrcode_filename = working_dir + str(ticket.ticket_gen_id) + '.png'
        pdf_filename = working_dir + str(ticket.ticket_gen_id) + '.pdf'

        url = pyqrcode.create(str(ticket.ticket_gen_id))
        url.png(qrcode_filename, scale=8)

        created_pdf = PDF(language=language)

        created_pdf.create(
            primary_color=cshop.primary_color,
            banner_image=cshop.header_img.url, # settings.MEDIA_ROOT+'/template/banner.jpg',
            event_title=event.title,
            event_date=formatted_date,
            event_time=formatted_time,
            event_price='€ '+str(utils.currency(ticket.price)),
            event_location=event.location,
            name=ticket.first_name + " " + ticket.last_name,
            ticket_type=ticket.ticket_type.name,
            qrcode=qrcode_filename
        )

        try:
            created_pdf.output(pdf_filename, 'F')
        except Exception as e:
            writeOrderLog(order_id=order.id, type=Orderlog.TYPE_MAIL_PDF_ERROR)

    writeOrderLog(order_id=order.id, type=Orderlog.TYPE_MAIL_PDF_CREATED)

class PDF(FPDF):

    primary_color = (0, 0, 0)

    start_y = 100
    start_x = 0
    body_set = False

    language = 'nl'

    font_to_use = 'DejaVu'

    def __init__(self, language):

        super(PDF, self).__init__()
        #DejaVuSansCondensed
        #self.add_font('Arial', '', 'Arial Unicode MS.ttf', uni=True)
        self.add_font(family='DejaVu', fname=os.path.join(os.path.dirname(__file__),'font/DejaVu.ttf'), uni=True)
        # self.add_font('a_true', 'B', 'Arial Unicode MS.ttf', uni=True)
        # self.add_font('a_true', '', 'Arial Unicode MS.ttf', uni=True)
        self.language = language

    def body(self):
        self.image(settings.TICKET_ASSETS_DIR+'ticket.png',0,0,210,297)

    def create(self, primary_color, banner_image, event_title, event_date, event_time, event_price, event_location,
               name, ticket_type, qrcode):

        color = primary_color.strip('#')

        if len(color) == 3:  # short group
            color = [str(str(c) + str(c)) for c in color]
            color = ''.join(color)

        self.primary_color = struct.unpack('BBB', bytes.fromhex(color))

        # add first page
        self.add_page()
        # add the body
        self.body()

        self.start_x = self.x

        self.create_banner(banner_image)
        self.create_event_title(event_title.upper())
        self.create_event_date(event_date)
        self.create_event_time(event_time)
        self.create_event_price(event_price)
        self.create_event_location(event_location.upper())
        self.create_name(name.upper(), ticket_type.upper())
        self.create_qr(qrcode)
        self.create_qr_text(utils.getWord(self.language, "pdf-ticket-qrtext"))

    def create_banner(self, image_path):
        #temp solution to allow sending ticket if event banner is not found 
        yourtickets_banner_path = settings.EMAIL_MEDIA_IMAGE_DIR + 'ticket_banner.png'
        try:
            self.image(image_path, 7, 10, 196)
        except:
            self.image(yourtickets_banner_path, 7, 10, 196)

    # black
    def create_event_title(self, title):
        # bold
        # w = self.get_string_width(title) + 6
        # self.set_x((210 - w) / 2)
        self.set_y(self.start_y)
        self.set_font(self.font_to_use, '', 30) # was bold
        self.set_text_color(0, 0, 0)
        # Output justified text

        self.multi_cell(0, 5, title)

        pass

    def create_event_date(self, date):

        self.set_xy(self.start_x, self.start_y+20)

        # self.set_y(self.start_y+20)
        self.set_font(self.font_to_use, '', 12) # bold
        self.set_text_color(0, 0, 0)
        self.cell(0,5, utils.getWord(self.language, "pdf-ticket-date", "datum"))

        self.set_xy(self.start_x, self.start_y+30)
        self.set_font(self.font_to_use, '', 20)
        self.set_text_color(self.primary_color[0], self.primary_color[1], self.primary_color[2])
        self.cell(0,5, date)

    def create_event_time(self, time_string):

        self.set_xy(self.start_x+80, self.start_y+20)

        # self.set_y(self.start_y+20)
        self.set_font(self.font_to_use, '', 12) # bold
        self.set_text_color(0, 0, 0)
        self.cell(0,5, utils.getWord(self.language, "pdf-ticket-time", "tijd"))

        self.set_xy(self.start_x+80, self.start_y+30)
        self.set_font(self.font_to_use, '', 20)
        self.set_text_color(self.primary_color[0], self.primary_color[1], self.primary_color[2])
        self.cell(0,5, time_string)

    def create_event_price(self, price):

        self.set_xy(self.start_x+140, self.start_y+20)

        self.set_font(self.font_to_use, '', 12) # bold
        self.set_text_color(0, 0, 0)
        self.cell(0,5, utils.getWord(self.language, "pdf-ticket-price", "prijs"))

        self.set_xy(self.start_x+140, self.start_y+30)
        self.set_font(self.font_to_use, '', 20)
        self.set_text_color(self.primary_color[0], self.primary_color[1], self.primary_color[2])
        self.cell(0,5, price)

    def create_event_location(self, location):

        self.set_xy(self.start_x, self.start_y+50)
        self.set_font(self.font_to_use, '', 12) # bold
        self.set_text_color(0, 0, 0)
        self.cell(0,5, utils.getWord(self.language, "pdf-ticket-location", "locatie"))

        self.set_xy(self.start_x, self.start_y+60)
        self.set_font(self.font_to_use, '', 20)
        self.set_text_color(self.primary_color[0], self.primary_color[1], self.primary_color[2])
        self.cell(0,5, location)

    def create_name(self, name, ticket_type):

        self.set_xy(self.start_x, self.start_y+90)
        self.set_font(self.font_to_use, '', 25)
        self.set_text_color(0, 0, 0)
        self.cell(0,5, name)

        self.set_xy(self.start_x, self.start_y+100)
        self.set_font(self.font_to_use, '', 12)
        self.set_text_color(0, 0, 0)
        self.cell(0,5, ticket_type)

    def create_qr(self, qr):
        self.image(qr,10,self.start_y+110,60,60)

    def create_qr_text(self, qrtext):
        self.set_xy(self.start_x+70, self.start_y+110)
        self.set_font(self.font_to_use, '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, qrtext)

