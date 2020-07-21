#!/usr/bin/python3

import logging
import sys
import os

# virtualenv
if os.getenv('FLASK_ENV') != 'development':
	activate_this = os.getenv('VENV_ROOT') + 'sundance-venv/bin/activate_this.py'
	with open(activate_this) as f:
		exec(f.read(), dict(__file__=activate_this))

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/truck_routing_application/')

from app import app as application