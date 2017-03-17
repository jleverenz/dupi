import hashlib
import os


# TODO refactor with finddup -- note that a bug was found in this code with
# visited_directories
def generate_filelist(directories):
    """Walk `directories` recursively and return a `list` of filenames
    found.
    """
    rv = []

    # Reminder: os.walk does not guarantee order of files in any single
    # directory. This method calls sort_filelist_peers to ensure
    # ordering. Additionally, it will maintain stable order based on input
    # 'directories' order.

    # Reminder: by default, os.walk skip symlinks to directories

    visited_directories = set()

    # NOTE os.walk `followlinks` default is False, will not descend into
    # directory links
    for directory in directories:
        for dirpath, dirlist, filelist in os.walk(directory):
            # TODO - repeatedly tries to add the visited dir?
            abspath = os.path.abspath(dirpath)
            if abspath in visited_directories:
                continue
            visited_directories.add(abspath)

            dirlist[:] = [d for d in dirlist
                          if os.path.abspath(d) not in visited_directories]

            for fname in [f for f in sort_filelist_peers(filelist)
                          if not os.path.islink(os.path.join(dirpath, f))]:
                rv.append(os.path.join(dirpath, fname))
    return rv


def sort_filelist_peers(filelist):
    """Sort a list of filenames to ensure ordering.

    This is used to guarantee predictable results from the arbitrary ordering
    of os.walk and os.listdir.
    """

    return sorted(filelist)


def hash_file(filepath):
    """Compute the sha256 hash of file at `filepath`, read in 64K blocks."""
    BLOCKSIZE = 65536
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    return hasher.hexdigest()
