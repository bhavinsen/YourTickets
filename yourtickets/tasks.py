from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery import shared_task
from celery.utils.log import get_task_logger

from ticketshop.models import (Order, Orderlog)
from yourtickets.common.log import writeOrderLog
from yourtickets.common.ticket import send_mail_and_create_pdfs, send_mail_and_create_pdf_for_ticket

logger = get_task_logger(__name__)

app = Celery()

@shared_task
def send_mail_orders_test():

    #writeOrderLog(mollie_id=1234, type=Orderlog.TYPE_WEBHOOK_MOLLIE_API_RECEIVED)
    print('yeahhhhh')


@app.task
def send_mail_order(order_id, base_url=None, email=None):
    writeOrderLog(order_id=order_id, type=Orderlog.TYPE_TASK_MANAGER_START)
    order = Order.objects.filter(pk=order_id).first()

    send_mail_and_create_pdfs(order, email=email, base_url=base_url)

    # set the mail to send
    order.mail_send = True
    order.save()
    writeOrderLog(order_id=order.id, type=Orderlog.TYPE_TASK_MANAGER_DONE)

    print('yeahhhhh')
    print(order_id)
