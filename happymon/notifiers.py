import smtplib

from email.mime.text import MIMEText

from datetime import datetime

# catch socket errors when postfix isn't running...
from socket import error as socket_error


def stdout(context, notifier):
    message = context.name + ': ' + ', '.join([str(i) for i in set(context.incidents)])
    print("ALERT: {}".format(message))

def smtp(context, notifier):

    incident = context.incidents[0]

    # TODO: support custom body templates?
    message = '{}: {}<br><br>'.format(context.name, context.extra)
    message += 'incidents: <br><br>' + '<br>'.join([str(i) for i in context.incidents])

    # TODO: support multipart message with both text and HTML.
    msg = MIMEText(message, 'html')

    # TODO: support custom subjects?
    msg['Subject'] = "{} | {} | {} | happymon".format(context.name, incident, incident.timestamp)

    # TODO: if 'from' raises key error, what do we do?
    msg['From']    = notifier.extra['from']

    # allow the extra 'to' to be a string or a list of strings.
    # TODO: if 'to' raises key error, what do we do?
    if isinstance(notifier.extra['to'], list):
        msg['To']  = ', '.join(notifier.extra['to'])
    else:
        msg['To']  = notifier.extra['to']

    # TODO: react to socket error when postfix/sendmail not running.
    s = smtplib.SMTP('localhost')

    s.sendmail(notifier.extra['from'], notifier.extra['to'], msg.as_string())
    s.quit()
