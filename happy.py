from twisted.web.client import getPage
from twisted.internet import task
from twisted.internet import reactor

from config import get_config

def rails_health_checks(result, params):
    print('##########################')
    print(params['uri'])
    print(result)
    print(params)
    reactor.callLater(params.get('frequency', 60), http, params)
    print('##########################')

def rails_health_checks_err(result, params):

    print('##########################')
    print(params['uri'])
    print(result)
    print(result.value)
    print(params)
    reactor.callLater(params.get('frequency', 60), http, params)
    print('##########################')

registered_callbacks = {
  'rails_health_checks' : rails_health_checks,
}

registered_errbacks = {
  'rails_health_checks' : rails_health_checks_err,
}

def get_backs(params):
    """return a callback,errback tuple from registered"""
    callback_name = params['callback']
    errback_name = config.get('errback', callback_name)
    callback = registered_callbacks[callback_name]
    errback = registered_errbacks[errback_name]
    return (callback, errback)

def http(params):
    uri = params['uri']
    callback, errback = get_backs(params)
    d = getPage(uri, timeout=params.get('timeout', 15))
    d.addCallback(callback, params)
    d.addErrback(errback, params)

if __name__ == '__main__':
    # load config dictionary and defaults.
    config = get_config('config.yml')

    for target, params in config['checks']['http'].items():
        http(params)

    # enter main reactor loop which never ends.
    reactor.run()
