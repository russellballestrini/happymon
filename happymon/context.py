class CheckContext(object):

    def __init__(self, name):
        # TODO: one line comment describing each of these attributes.
        self.name = name
        self.alarming = False
        self.threshold = 3
        self.frequency = 60
        self.timeout   = 20
        self.collector = None
        self.handler   = None
        self.error_handler = None
        self.notifiers = []
        self.incidents = []
        self.archived_incidents = []
        self.extra = {}

    @property
    def hit_threshold(self):
        """check if we have hit or exceeded the incident threshold."""
        return len(self.incidents) >= self.threshold

    def fire_alarm(self):
        """fire all notifiers and sets alarming state."""
        for notifier in self.notifiers:
            notifier.handler(self, notifier)
        self.alarming = True

    def clear_alarm(self):
        """clear all incidents and clear alarming state."""
        self.alarming = False
        self.archived_incidents += self.incidents
        self.incidents = []

    def house_keeping(self):
        """house keeping."""
        if self.hit_threshold and not self.alarming:
            self.fire_alarm()

class NotifierContext(object):
    def __init__(self, name):
        # TODO: one line comment describing each of these attributes.
        self.name = name
        self.handler = None
        self.extra = {}


