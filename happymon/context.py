class Context(object):

    def __init__(self, name):
        self.name = name
        self.incidents = []
        self.alerts = []
        self.extra = {}
        self.collector = None
        self.handler = None
        self.error_handler = None
        self.alert_handler = None
        self.threshold = 3
        self.frequency = 60
        self.timeout   = 20
