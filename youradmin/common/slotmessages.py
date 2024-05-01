from django.contrib.messages import get_messages


def slotmessages(request):
    message_list = get_messages(request)
    ordered_messages = {}
    for message in message_list:
        if not ordered_messages.get(message.tags):
            ordered_messages[message.tags] = []
        ordered_messages[message.tags].append(message)

    return {'slotmessages': ordered_messages}
