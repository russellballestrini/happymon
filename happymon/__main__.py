from argparse import ArgumentParser

from pkg_resources import iter_entry_points

from .config import get_config

from .context import Context

from twisted.internet import reactor

def load_entry_points(group_name):
    """Return a dictionary of entry_points related to given group_name"""
    entry_points = {}
    for entry_point in iter_entry_points(group=group_name, name=None):
        entry_points[entry_point.name] = entry_point.load()
    return entry_points

def main():
    """main cli console script entry point."""
    parser = ArgumentParser(description="don't worry, be happy, mon!")
    parser.add_argument('-c', '--config', default='config.yml')
    args = parser.parse_args()

    # load config dictionary and defaults from file path.
    config = get_config(args.config)

    # load and register collectors and handlers.
    collectors = load_entry_points('happymon.collectors')
    handlers = load_entry_points('happymon.handlers')
    error_handlers = load_entry_points('happymon.error_handlers')

    # iterate over all checks.
    for check_name, params in config['checks'].items():

        collector_name = params['collector']
        handler_name = params['handler']

        # create a new context object to hold information about this check.
        context = Context(check_name)

        # attach function to context object.
        context.collector      = collectors[params['collector']]
        context.handler        = handlers[params['handler']]
        context.error_handler  = error_handlers[params['handler']]

        # get value or default.
        context.threshold = params.get('threshold', config['threshold'])
        context.frequency = params.get('frequency', config['frequency'])
        context.timeout   = params.get('timeout', config['timeout'])

        # extra parameters specific to this collector / handler.
        context.extra = params['extra']

        # a collector must take the context as first argument.
        # we expect collector functions behave asynchronously.
        context.collector(context)

    # enter main reactor loop which never ends.
    reactor.run()

if __name__ == '__main__':
    main()
