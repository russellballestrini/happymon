from argparse import ArgumentParser

from pkg_resources import iter_entry_points

from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

from .config import get_config

def load_entry_points(group_name):
    """Return a dictionary of entry_points related to given group_name"""
    entry_points = {}
    for entry_point in iter_entry_points(group=group_name, name=None):
        entry_points[entry_point.name] = entry_point.load()
    return entry_points

from twisted.internet.ssl import ClientContextFactory

class WebClientContextFactory(ClientContextFactory):
    def getContext(self, hostname, port):
        return ClientContextFactory.getContext(self)

def http(params):
    # Reference:
    #   https://twistedmatrix.com/documents/current/web/howto/client.html
    agent = Agent(reactor, WebClientContextFactory())
    d = agent.request(
        'GET',
        params['uri'],
        Headers({'User-Agent' : ['happymon']}),
        None
    )
    d.addCallback(params['handler_callback'], params)
    d.addErrback(params['handler_errback'], params)

def main():
    """main cli console script entry point."""
    parser = ArgumentParser(description="don't worry, be happy, mon!")
    parser.add_argument('-c', '--config', default='config.yml')
    args = parser.parse_args()

    # load config dictionary and defaults.
    config = get_config(args.config)

    # load callbacks / errbacks from 3rd party entry_points.
    handler_callbacks = load_entry_points('happymon.callbacks')
    handler_errbacks = load_entry_points('happymon.errbacks')

    collector_funcs = {
      'http' : http,
    }

    # iterate over all collectors (checks).
    for collector_name in config['checks']:

        # get the collector function by name from collector_funcs registry.
        collector_func = collector_funcs[collector_name]

        # iterate over all the targets for this collector.
        for target, params in config['checks'][collector_name].items():

            # attach collector function to params.
            params['collector'] = collector_func

            # attach handler_callback and handler_errback to params.
            handler_name = params['handler']
            params['handler_callback'] = handler_callbacks[handler_name]
            params['handler_errback']  = handler_errbacks[handler_name]

            # todo: maybe all this config mutation should be in the config mod?
            # create a empty list for incidents.
            params['incidents'] = []

            # finally call the collector and pass this target's params.
            # we expect collector functions to be async.
            collector_func(params)

    # enter main reactor loop which never ends.
    reactor.run()

if __name__ == '__main__':
    main()
