

activate_this = '/usr/local/env/flask/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, "/var/www/html/blog/")

from blog import app as application
