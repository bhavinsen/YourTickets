
class Cart:

    storage = None
    key = 'cart'

    def __init__(self, request):

        if self.key not in request.session:
            request.session[self.key] = {}
        self.storage = request.session[self.key]

    def add_email_allowed(self, event_id, email_allowed):
        event_id = str(event_id)
        self._create_event_if_not_exists(event_id)
        self.storage[event_id]['email_allowed'] = email_allowed

    def get_email_allowed(self, event_id):
        event_id = str(event_id)
        self._create_event_if_not_exists(event_id)

        if 'email_allowed' not in self.storage[event_id]:
            return False
        else:
            return self.storage[event_id]['email_allowed']

    def _create_event_if_not_exists(self, event_id):
        event_id = str(event_id)
        if event_id not in self.storage:

            self.storage[event_id] = {}

    def flush_event(self, event_id):
        event_id = str(event_id)
        if event_id in self.storage:
            self.storage[event_id] = {}

    # list like {'ticket.pk':4}
    def set_tickets(self, event_id, tickets_id_amount):
        event_id = str(event_id)
        self._create_event_if_not_exists(event_id)

        self.storage[event_id]['tickets'] = tickets_id_amount

    def get_tickets(self, event_id):
        event_id = str(event_id)
        self._create_event_if_not_exists(event_id)

        if 'tickets' in self.storage[event_id]:
            return self.storage[event_id]['tickets']

        return list()

    def has_event_and_tickets(self, event_id):
        event_id = str(event_id)
        if event_id in self.storage:
            if len(self.get_tickets(event_id)) > 0:
                return True

        return False
