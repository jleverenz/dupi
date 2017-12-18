from collections import defaultdict
import os

from dupi.utils import hash_file, generate_filelist


def purge_removed_files(index):
    for i in list(index.all()):
        if not os.path.exists(i['fullpath']):
            index.remove(i['fullpath'])


def update_index(index, directories=[]):
    purge_removed_files(index)

    if(len(directories) == 0):
        for i in list(index.all()):
            try:
                stats = os.stat(i['fullpath'])
            except FileNotFoundError:
                # disappeared, purge it
                index.remove(i['fullpath'])
                continue

            if(stats.st_mtime != i['mtime']):
                index.update({'fullpath': i['fullpath'],
                              'size': stats.st_size,
                              'mtime': stats.st_mtime,
                              'sha256': hash_file(i['fullpath'])})

    for f in generate_filelist(directories):
        fullpath = os.path.abspath(f)

        try:
            stats = os.stat(f)
        except FileNotFoundError:
            continue

        existing = index.get(fullpath)

        if existing is not None:
            if(stats.st_mtime != existing['mtime']):
                index.update({'fullpath': fullpath,
                              'size': stats.st_size,
                              'mtime': stats.st_mtime,
                              'sha256': hash_file(fullpath)})
        else:
            index.update({'fullpath': fullpath,
                          'size': stats.st_size,
                          'mtime': stats.st_mtime,
                          'sha256': hash_file(fullpath)})


def list_duplicates(index):
    """Generate the duplicate files found in the index."""

    for orig_dup_list in index.get_duplicate_hash_dict().values():
        for dup in orig_dup_list[1:]:
            yield dup


def list_duplicates_with_originals(index):
    """Returns list of lists. Inner list contains [orig, dup, dup, ...]"""

    return list(index.get_duplicate_hash_dict().values())
