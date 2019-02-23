import unittest
from howl import Monitor


class TestMonitor(unittest.TestCase):
    def setUp(self):
        self.monitor = Monitor()

    def test_checkin(self):
        self.monitor.checkin()
