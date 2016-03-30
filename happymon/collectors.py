from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

from twisted.internet.ssl import ClientContextFactory

class WebClientFactory(ClientContextFactory):
    def getContext(self, hostname, port):
        return ClientContextFactory.getContext(self)

def http(context):
    # Reference:
    #   https://twistedmatrix.com/documents/current/web/howto/client.html
    agent = Agent(reactor, WebClientFactory())
    d = agent.request(
        'GET',
        context.extra['uri'],
        Headers({'User-Agent' : ['happymon']}),
        None
    )
    d.addCallback(context.handler, context)
    d.addErrback(context.error_handler, context)
