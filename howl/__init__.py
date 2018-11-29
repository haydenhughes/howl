import pyotp
from flask import Flask
from .alerts import Monitor, parse
from logging.config import dictConfig
from flask_httpauth import HTTPBasicAuth

# Configure flask's logger
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'NOTSET',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.config.from_object('config.Config')
app.logger.setLevel(app.config['LOG_LEVEL'])
auth = HTTPBasicAuth()
monitor = Monitor(check_interval=app.config['CHECK_INTERVAL'])
totp = pyotp.TOTP(app.config['TOTP_SECRET'])


@auth.get_password
def get_pw(user):
    """Checks if username is correct and generates a password using totp."""
    if user == app.config['USERNAME']:
        return totp.now()

    return None


@app.route('/trigger/<alert>')
@auth.login_required
def trigger(alert):
    """Manually trigger an alert.

    Args:
        alert: A string of the alert file (without the .yml).
    """
    for service in parse(alert)['services']:
        try:
            service.send()
        except Exception as e:
            return e.msg

    return 'DONE, I hope you know what your doing...'


@app.route('/checkin')
@auth.login_required
def checkin():
    """Trigger a check in."""
    monitor.checkin()
    return 'DONE, last check in: {}'.format(monitor.last_checkin)
