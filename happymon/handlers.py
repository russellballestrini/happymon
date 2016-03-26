from twisted.internet import reactor

def http_code(response, params):
    """
    This is mostly an example on how to write a handler_callback.

    Check if the response's HTTP status code is in the list of desired_codes.
    """
    print params['uri'], response.code, response.phrase
    if response.code not in params.get('desired_codes', [200]):
        params['incidents'].append('meh an incident happened, meh.. meh!')    
        print(params['incidents'])
    reactor.callLater(params['frequency'], params['collector'], params) 
    
def http_code_err(response, params):
    """
    this is mostly an example on how to write a handler_errback.
    """
    # it's always an incident when the errback is called, I guess.
    print(params['uri'])
    params['incidents'].append('meh an incident happened, meh.. meh!')    
    print(params['incidents'])
    reactor.callLater(params['frequency'], params['collector'], params) 
