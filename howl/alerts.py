import yaml
import os
import glob
import time
import threading
from datetime import datetime
from .services import *  # Required for yaml.load


class Monitor(threading.Thread):
    """Checks when the last check in was and acts accordingly.

    Monitor runs as a thread to avoid hanging the api.

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
        for alert in all():
            if alert.timeout is not None:
                if delta_time >= datetime.difftime(alert['timeout']):
                    for service in alert.services:
                        service.send()

    def run(self):
        """Called by Monitor.start() to start the thead."""
        while True:
            time.sleep(self.check_interval)
            self._check()


class Alert(object):
    """Wraps the alert configuration.

    Attributes:
        name: A string of the alert name.
        timeout: An interger of the alert timeout.
        services: A list of service objects associated with the alert.
    """

    def __init__(self, name):
        with open('alerts/{}.yml'.format(name)) as fp:
            config = yaml.load(fp)

        self.name = name
        self.timeout = config['timeout']
        self.services = config['services']


def all():
    """A generator to get all the alerts in `alerts/`

    Yeilds:
        Alert objects of all the alerts.
    """
    for alert in glob.glob(os.path.join('alerts/*.yml')):
        yield Alert(alert)
