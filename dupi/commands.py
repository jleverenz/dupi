import os

from dupi import conf, core


_command_dict = dict()


def dispatch(index, command, **kwargs):
    _command_dict[command](index, **kwargs)


def _dupi_command(fn):
    _command_dict[fn.__name__] = fn
    return fn


@_dupi_command
def update(index, **kwargs):
    if 'dirs'in kwargs:
        core.update_index(index, kwargs['dirs'])
    else:
        core.purge_removed_files(index)


@_dupi_command
def purge(index, **kwargs):
    index.purge()


@_dupi_command
def list(index, **kwargs):
    for i in core.list_duplicates(index):
        print(i)


@_dupi_command
def report(index, **kwargs):
    for orig, *dupes in core.list_duplicates_with_originals(index):
        print("o {}".format(orig))
        for i in dupes:
            print("d {}".format(i))


@_dupi_command
def stats(index, **kwargs):
    all = index.all()

    print("{} file records".format(len(all)))

    print("{} unique file sizes".format(len(set([i['size'] for i in all]))))

    print("\nFiles in the following directories:")
    for i in sorted(set([os.path.dirname(i['fullpath']) for i in all])):
        print("  {}".format(i))
