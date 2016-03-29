from twisted.internet import reactor

def http_code(response, context):
    """
    This is mostly an example on how to write a handler.

    Check if the response's HTTP status code is in the list of desired_codes.
    """
    print context.extra['uri'], response.code, response.phrase
    if response.code not in context.extra.get('desired_codes', [200]):
        context.incidents.append('meh an incident happened, meh.. meh!')
        print(context.incidents)
    reactor.callLater(context.frequency, context.collector, context)

def http_code_err(response, context):
    """
    This is mostly an example on how to write an error_handler.
    """
    # it's always an incident when the errback is called, I guess.
    context.incidents.append('meh an incident happened, meh.. meh!')
    print context.extra['uri'], context.incidents
    reactor.callLater(context.frequency, context.collector, context)
