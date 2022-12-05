import unittest
from date import *
import date

class TestMethods(unittest.TestCase):

    def test_str_to_date(self):
        self.assertEqual(str_to_date("2015-02-10T13:00:00Z"), date.datetime(2015, 2, 10, 13, 0))

    def test_date_to_str(self):
        self.assertEqual(date_to_str(date.datetime(2015, 2, 10, 12, 30)), "2015-02-10T12:30:00Z")

    def test_date_to_str_hours(self):
        self.assertEqual(date_to_str_hours(date.datetime(2015, 2, 10, 12, 30)),"2015-02-10T12:00:00Z")
        self.assertEqual(date_to_str_hours(date.datetime(2015, 2, 10, 13, 40)), "2015-02-10T13:00:00Z")
        self.assertEqual(date_to_str_hours(date.datetime(2015, 2, 10, 12, 10)), "2015-02-10T12:00:00Z")
        self.assertEqual(date_to_str_hours(date.datetime(2015, 2, 10, 9, 00)), "2015-02-10T09:00:00Z")

    def test_str_to_str_days(self):
        self.assertEqual(str_to_str_days("2015-02-10T12:00:00Z"),"2015-02-10T00:00:00Z")
        self.assertEqual(str_to_str_days("2015-02-10T00:18:00Z"),"2015-02-10T00:00:00Z")
        self.assertEqual(str_to_str_days("2015-02-10T00:00:45Z"),"2015-02-10T00:00:00Z")
    
    def test_frequency_time(self):
        self.assertEqual(frequency_time("2015-02-10T12:30:10Z", "hourly"),"2015-02-10T12:00:00Z")
        self.assertEqual(frequency_time("2015-02-10T12:30:10Z", "daily"),"2015-02-10T00:00:00Z")
        self.assertEqual(frequency_time("2015-02-10T12:30:10Z", ""),"2015-02-10T12:30:10Z")

if __name__ == '__main__':
    unittest.main()