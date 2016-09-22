from ago import human

from time import time

class Incident(object):

    def __init__(self, name, context=None):
        # TODO: one line comment describing each of these attributes.
        self.name = name
        self.context = context
        self.timestamp = int(time() * 1000)

    @property
    def ago(self):
        """Accepts a timestamp and returns a human readable string"""
        return human(self.timestamp/1000.0, precision=1, abbreviate=True)

    def __str__(self):
        return '{} {}'.format(self.name, self.ago)

    def __repr__(self):
        return '{} {}'.format(self.name, self.ago)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)
