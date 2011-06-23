#!/usr/bin/env python
import sys
import os

# to quiet geopy
sys.stdout = sys.stderr

parent_dir=os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cugos_org.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
