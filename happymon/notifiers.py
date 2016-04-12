import smtplib

from email.mime.text import MIMEText

from datetime import datetime

# catch socket errors when postfix isn't running...
from socket import error as socket_error

def stdout(context, notifier):
    message = context.name + ': ' + ', '.join(set(context.incidents))
    print("ALERT: {}".format(message))

def smtp(context, notifier):

    NOW = datetime.now()

    # TODO: support custom body templates?
    message = context.name + ': ' + ', '.join(set(context.incidents))

    # TODO: support multipart message with both text and HTML.
    msg = MIMEText(message, 'html')

    # TODO: support custom subjects?
    msg['Subject'] = "{} | {} | {} | happymon".format(context.name, context.incidents[0], NOW)

    # TODO: if from / to raises key error, what do we do?
    msg['From']    = notifier.extra['from']
    msg['To']      = ', '.join(notifier.extra['to'])

    # TODO: react to socket error when postfix/sendmail not running.
    s = smtplib.SMTP('localhost')

    s.sendmail(notifier.extra['from'], notifier.extra['to'], msg.as_string())
    s.quit()
