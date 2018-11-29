import yaml
import os
import glob
import time
import threading
from datetime import datetime
from . import trigger
from .services import *  # Required for yaml.load


class Monitor(threading.Thread):
    """Checks when the last check in was and acts accordingly.

    Monitor runs as a thread to avoid sleeping the api.

    Attributes:
        check_interval: An integer of the amount of seconds to wait before
                        checking if a alert should be triggered. Defaults to
                        21600.
        last_checkin: A datetime object of the last check in. Defaults to
                      the current time.
    """

    def __init__(self,
                 check_interval=21600,
                 last_checkin=datetime.now()):
        super().__init__(target=self)
        self.check_interval = check_interval
        self.last_checkin = last_checkin

    def checkin(self):
        """Sets last_checkin to the current time."""
        self.last_checkin = datetime.now()

    def _check(self):
        """Checks to see if any alerts should be triggered."""
        delta_time = datetime.now() - self.last_checkin
        for alert in parse_all():
            if alert['timeout'] is not None:
                if delta_time >= datetime.difftime(alert['timeout']):
                    trigger(alert['name'])

    def run(self):
        """Called by Monitor.start() to start the thead."""
        while True:
            time.sleep(self.check_interval)
            self._check()


def parse(alert):
    """Parses the alerts.

    The services get converted to their respective objects.

    Args:
        alert: A string of the name of the alert to parse (without the .yml).
    """
    with open('alerts/{}.yml'.format(alert)) as fp:
        a = yaml.load(fp)
        a['name'] = alert
        return a


def parse_all():
    """A generator to parse all the alerts in `alerts/`"""
    for alert in glob.glob(os.path.join('alerts/*.yml')):
        yield parse(alert)
