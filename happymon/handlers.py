from twisted.internet import reactor

from incident import Incident

def http_code(response, context):
    """
    This is mostly an example on how to write a handler.

    Check if the response's HTTP status code is in the list of desired_codes.
    """
    print context.name, context.extra['uri'], response.code, response.phrase
    if response.code not in context.extra.get('desired_codes', [200]):
        context.incidents.append(Incident('desired code incident'))
    else:
        context.clear_alarm()
    context.house_keeping(reactor)
    #print(vars(context))

def http_code_err(response, context):
    """
    This is mostly an example on how to write an error_handler.
    """
    # it's always an incident when the errback is called, I guess.
    context.incidents.append(Incident('http_code_err'))
    print context.name, context.extra['uri'], context.incidents
    context.house_keeping(reactor)
