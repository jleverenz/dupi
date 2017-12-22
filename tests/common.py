import sys

# Backport from contextlib2 for python 3.4
if sys.version_info < (3, 5):
    from contextlib2 import redirect_stderr
else:
    from contextlib import redirect_stderr
