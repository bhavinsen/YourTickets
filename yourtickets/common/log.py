from ticketshop.models import Log, Orderlog

def writeLog(category, message):
    try:
        log = Log(category=category, message=message)
        log.save()

    except Exception as e:
        pass

def writeOrderLog(mollie_id='', order_id='', type='', description=''):
    try:
        log = Orderlog(mollie_id=mollie_id, order_id=order_id, type=type, description=description)
        log.save()
    except Exception as e:
        pass