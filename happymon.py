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

# load callbacks / errbacks from 3rd party entry_points.
happymon_callbacks = load_entry_points('happymon.callbacks')
happymon_errbacks = load_entry_points('happymon.errbacks')

def get_backs(params):
    """return a callback,errback tuple from registered"""
    callback_name = params['callback']
    errback_name = config.get('errback', callback_name)
    callback = happymon_callbacks[callback_name]
    errback = happymon_errbacks[errback_name]
    return (callback, errback)

def http(params):
    uri = params['uri']
    callback, errback = get_backs(params)
    d = getPage(uri, timeout=params.get('timeout', 15))
    d.addCallback(callback, params)
    d.addErrback(errback, params)

if __name__ == '__main__':

    parser = ArgumentParser(description="don't worry, be happy, mon!")
    parser.add_argument('-c', '--config', default='config.yml')
    args = parser.parse_args()

    # load config dictionary and defaults.
    config = get_config(args.config)

    for target, params in config['checks']['http'].items():
        http(params)

    # enter main reactor loop which never ends.
    reactor.run()
