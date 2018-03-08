"""High level functions for working with a dupi index."""

from collections import defaultdict
import os
from tqdm import tqdm

from dupi.utils import hash_file, generate_filelist


def purge_removed_files(index):
    """Remove index records for files that no longer exist."""
    for i in list(index.all()):
        if not os.path.exists(i['fullpath']):
            index.remove(i['fullpath'])


# Test for zero length before calling tqdm, otherwise it'll leave a "0it"
# console clutter around. tqdm's `leave` param doesn't help, since showing
# final progress bar of non-zero lists is desirable.
def _cleaner_tqdm(iterable):
    if iterable:
        for i in tqdm(iterable):
            yield i
    else:
        return []


def update_index(index, directories=[]):
    """Update the index with new file stats.

    If supplied, search recursively in `directories` for files and add stats to
    the index. If `directories` is not supplied check for file mods in existing
    indexed files and update stats if needed."""

    purge_removed_files(index)

    if(len(directories) == 0):
        for i in _cleaner_tqdm(list(index.all())):
            index._update(i['fullpath'])

    for f in _cleaner_tqdm(generate_filelist(directories)):
        index._update(f)


def list_duplicates(index):
    """Generate the duplicate files found in the index."""

    for orig_dup_list in index.get_duplicate_hash_dict().values():
        for dup in orig_dup_list[1:]:
            yield dup


def list_duplicates_with_originals(index):
    """Returns list of lists. Inner list contains [orig, dup, dup, ...]"""

    return list(index.get_duplicate_hash_dict().values())
