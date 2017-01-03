def http_code(response, context):
    """
    Check if the response's HTTP status code is in the list of desired_codes.
    """
    print('{} {} {}'.format(response.status, response.reason, context))
    if int(response.status) not in context.extra.get('desired_codes', [200]):
        context.new_incident('desired code incident')
    else:
        context.clear_alarm()
    context.house_keeping()
