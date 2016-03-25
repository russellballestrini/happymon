from argparse import ArgumentParser

from pkg_resources import iter_entry_points

from twisted.web.client import getPage
from twisted.internet import task
from twisted.internet import reactor

from config import get_config

def load_entry_points(group_name):
    """Return a dictionary of entry_points related to given group_name"""
    entry_points = {}
    for entry_point in iter_entry_points(group=group_name, name=None):
        entry_points[entry_point.name] = entry_point.load()
    return entry_points

def http(params):
    d = getPage(params['uri'], timeout=params.get('timeout', 15))
    d.addCallback(params['handler_callback'], params)
    d.addErrback(params['handler_errback'], params)

if __name__ == '__main__':

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

            # finally call the collector and pass this target's params.
            # we expect collector functions to be async.
            collector_func(params)

    # enter main reactor loop which never ends.
    reactor.run()
