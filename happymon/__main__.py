from argparse import ArgumentParser

from pkg_resources import iter_entry_points

from .config import get_config

from .context import (
  CheckContext,
  NotifierContext,
)

import asyncio

def load_entry_points(group_name):
    """Return a dictionary of entry_points related to given group_name"""
    entry_points = {}
    for entry_point in iter_entry_points(group=group_name, name=None):
        entry_points[entry_point.name] = entry_point.load()
    return entry_points

def emit_plugins(plugin_type, plugins):
    print('{}: {}'.format(plugin_type, ', '.join(plugins)))

def main():
    """main cli console script entry point."""
    parser = ArgumentParser(description="don't worry, be happy, mon!")
    parser.add_argument('-l', '--list-plugins', action='store_true', default=False)
    parser.add_argument('-c', '--config', default=None, metavar='/path/to/config.yml')
    args = parser.parse_args()

    # load and register collectors and handlers.
    collectors = load_entry_points('happymon.collectors')
    handlers = load_entry_points('happymon.handlers')
    error_handlers = load_entry_points('happymon.error_handlers')
    notifiers = load_entry_points('happymon.notifiers')

    if args.list_plugins == True:
        emit_plugins('collectors', collectors.keys())
        emit_plugins('handlers', handlers.keys())
        emit_plugins('notifiers', notifiers.keys())
        exit()

    if args.config is None:
        parser.print_help()
        exit()

    # get the asyncio event loop.
    loop = asyncio.get_event_loop()

    # load config dictionary and defaults from file path.
    config = get_config(args.config)

    notifier_registry = {}

    # iterate over all notifiers.
    for notifier_name, params in config.get('notifiers', {}).items():

        # create a new notifier context object.
        notifier = NotifierContext(notifier_name)

        # attach notifier handler function to context object.
        notifier.handler = notifiers[params['handler']]

        # extra parameters specific to this notifier.
        notifier.extra = params.get('extra', {})

        # register this notifier so we can reference it when building checks.
        notifier_registry[notifier_name] = notifier

    # iterate over all checks.
    for check_name, params in config.get('checks', {}).items():

        # create a new check context object.
        check = CheckContext(check_name, loop)

        # attach collector coroutines to the context object.
        check.collector = collectors[params['collector']]

        # attach handler functions to the context object.
        check.handler = handlers[params['handler']]

        # attach zero or many notifier functions to context object.
        for notifier_name in params.get('notifiers', []):
            check.notifiers.append(notifier_registry[notifier_name])

        # get value or default.
        check.threshold = params.get('threshold', config['threshold'])
        check.frequency = params.get('frequency', config['frequency'])
        check.timeout   = params.get('timeout', config['timeout'])

        # extra parameters specific to this collector / handler.
        check.extra = params.get('extra', {})

        # finally register the check's collector with the event loop.
        check.house_keeping()

    # enter main reactor loop which never ends.
    # this starts the chain reaction.
    loop.run_forever()


if __name__ == '__main__':
    main()
