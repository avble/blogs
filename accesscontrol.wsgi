import sys
import os
sys.path.insert(0, "/var/www/flaskAccessControl"+"/..")

activate_env=os.path.expanduser("/var/www/flaskAccessControl/venv/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

from flaskAccessControl import create_app

application = create_app()
