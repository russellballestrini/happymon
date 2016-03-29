class CheckContext(object):

    def __init__(self, name):
        # TODO: one line comment describing each of these attributes.
        self.name = name
        self.threshold = 3
        self.frequency = 60
        self.timeout   = 20
        self.collector = None
        self.handler   = None
        self.error_handler = None
        self.notifiers = []
        self.incidents = []
        self.extra = {}


class NotifierContext(object):
    def __init__(self, name):
        # TODO: one line comment describing each of these attributes.
        self.name = name
        self.handler = None
        self.extra = {}


