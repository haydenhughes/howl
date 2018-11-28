from datetime import datetime
import time
import threading
import howl


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
        for alert in howl.alerts.parse_all():
            if alert['timeout'] is not None:
                if delta_time >= datetime.difftime(alert['timeout']):
                    howl.trigger(alert['name'])

    def run(self):
        """Called by Monitor.start() to start the thead."""
        while True:
            time.sleep(self.check_interval)
            self._check()
