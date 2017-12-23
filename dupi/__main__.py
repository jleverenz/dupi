import argparse
from dupi.commands import dispatch
from dupi import conf
from dupi.index import Index


def _parse_args(args=None):
    """Parse `args` as command line options. If `args` is None,
    use sys.argv"""

    desc = 'File hash indexer for duplicate file finding.'
    parser = argparse.ArgumentParser(prog='dupi', description=desc)

    subparsers = parser.add_subparsers(dest='command')

    update_parser = subparsers.add_parser('update',
                                          help='update index with dirs')
    update_parser.add_argument('dirs', nargs='*',
                               help='directories to recursively search for '
                               'files to idnex')

    subparsers.add_parser('purge', help='purge index')
    subparsers.add_parser('list', help='list duplicates in index')
    subparsers.add_parser('report',
                          help='report duplicates with originals in index')
    subparsers.add_parser('stats', help='stats for index')

    if args is None:
        return parser.parse_args()  # pragma: no cover - args from cli only
    else:
        return parser.parse_args(args)


def main(args=None):
    dict_args = vars(_parse_args(args))

    command = dict_args['command']
    del dict_args['command']

    s = Index(conf.index_file)
    dispatch(s, command, **dict_args)
    s.save()


if __name__ == "__main__":  # pragma: no cover
    main()
