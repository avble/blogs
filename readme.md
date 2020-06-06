Flask-AccessControl
=========
This server is to allow a mobile device (main) to share its right of accessing IoT hub to another mobile device

![image](https://user-images.githubusercontent.com/5534923/83938639-826efe80-a800-11ea-9136-efb27b903dbd.png)

Development
-----------
On Linux 
    $ export FLASK_ENV=development
    $ flask db-init-data
    $ flask run

Or on Windows cmd::

    > set FLASK_ENV=development
    > flask db-init-data
    > flask run

Open http://127.0.0.1:5000 in a browser.

note: 
if '$flask run' does not run, please use 'python -m flask run' in stead. 


Test
----
Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser
