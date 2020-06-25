import os
import sys
cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, cur_dir + "/..")

from flaskAccessControl import create_app

app = create_app()

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0')
