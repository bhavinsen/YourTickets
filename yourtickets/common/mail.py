import os
import pyqrcode
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.template import loader
from django.conf import settings
from django.core.mail import EmailMessage


def _build_images(html_part, banner=None):

    if (not banner) or (not os.path.exists( settings.BASE_DIR + banner)):
        img_data = open(settings.EMAIL_MEDIA_IMAGE_DIR + 'ticket_banner.png', 'rb').read()  
    else:    
        try:
            img_data = open(settings.BASE_DIR + banner, 'rb').read()
        except Exception as e:
            img_data = open(settings.EMAIL_MEDIA_IMAGE_DIR + 'ticket_banner.png', 'rb').read()   
            
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

    return html_part

def create_mail(template_context, subject, send_to, attachments=None, banner=None):

    html_part = MIMEMultipart(_subtype='related')
    email_template = loader.render_to_string('emails/template.html', template_context)
    body = MIMEText(email_template.encode('utf-8'), _subtype='html', _charset='utf-8')
    html_part.attach(body)

    
        

    html_part = _build_images(html_part=html_part, banner=banner)



    msg = EmailMessage(
        subject=subject,
        from_email="noreply@yourtickets.nl",
        to=[send_to],
        bcc=['tickets@yourtickets.nl'],

    )
    msg.attach(html_part)
    msg.send()


# this is the new way from 2018 to send mails
def send_template_mail(template, context, subject, send_to):
    html_part = MIMEMultipart(_subtype='related')
    email_template = loader.render_to_string(template, context)
    body = MIMEText(email_template.encode('utf-8'), _subtype='html', _charset='utf-8')
    html_part.attach(body)

    html_part = _build_images(html_part=html_part)

    msg = EmailMessage(
        subject=subject,
        from_email="noreply@yourtickets.nl",
        to=[send_to],
        bcc=['tickets@yourtickets.nl'],

    )
    msg.attach(html_part)
    msg.send()



def create_ticket_mail(template, shop_image, template_context, subject, send_to, attachments):

    html_part = _build_images()
    # image vervangen door parameter

    # img_data = open(settings.CUSTOM_SHOP_UPLOAD_DIR + cshop.header_img.url, 'rb').read()
    # img = MIMEImage(img_data, 'png')
    # img.add_header('Content-Id', '<logo>')
    # img.add_header("Content-Disposition", "inline", filename="logo")
    # html_part.attach(img)

    email_template = loader.render_to_string('emails/direct_ticket.html', template_context)
    body = MIMEText(email_template.encode('utf-8'), _subtype='html', _charset='utf-8')
    html_part.attach(body)

    msg = EmailMessage(
        subject=subject,
        from_email="noreply@yourtickets.nl",
        to=['almerelc@gmail.com'],  # needs to be send_to
        bcc=['tickets@yourtickets.nl'],
        attachments=attachments
    )
    msg.attach(html_part)
    msg.send()