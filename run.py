# run.py
# CS 6360 FINAL PROJECT
#
# Michael Holcomb (mjh170630)
# Harshavardhan Nalajala (hxn170230)
# Vigneshwaran Sampath (vxs180021)

import os

from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)


def waitress():
    config_name = os.getenv('FLASK_CONFIG')
    return create_app(config_name)


if __name__ == '__main__':
    app.run()
