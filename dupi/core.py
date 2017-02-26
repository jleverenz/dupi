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
            indexed_mtime = i['mtime']
            stats = os.stat(i['fullpath'])
            if(stats.st_mtime != i['mtime']):
                index.update({'fullpath': i['fullpath'],
                              'size': stats.st_size,
                              'mtime': stats.st_mtime,
                              'sha256': hash_file(i['fullpath'])})

    for f in generate_filelist(directories):
        fullpath = os.path.abspath(f)
        stats = os.stat(f)
        existing = index.get(fullpath)

        if existing is not None:
            if(stats.st_mtime != existing['mtime']):
                index.update({'fullpath': fullpath,
                              'size': stats.st_size,
                              'mtime': stats.st_mtime,
                              'sha256': hash_file(fullpath)})
        else:
            index.insert({'fullpath': fullpath,
                          'size': stats.st_size,
                          'mtime': stats.st_mtime,
                          'sha256': hash_file(fullpath)})


def list_duplicates(index):
    """Generate the duplicate files found in the index."""
    hashes = set()
    for i in index.all():
        h = i['sha256']
        if h in hashes:
            yield i['fullpath']
        else:
            hashes.add(h)


def list_duplicates_with_originals(index):
    # NOTE that the order of the return is not guaranteed due to unordered dict
    d = defaultdict(list)  # hash, [orig, dup, dup, ...]
    for i in index.all():
        d[i['sha256']].append(i['fullpath'])

    return [i for i in d.values() if len(i) > 1]
