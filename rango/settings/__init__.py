# From: https://www.djangorocks.com/snippets/seamless-switching-between-live-and-development.html

import os
from main import *

if os.environ.get('DJANGO_DEV', False):
    print "Using dev environment"
    from dev import *
else:
    print "Using live environment"
    from live import *
