import yaml
import os
import glob
from .services import *


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
