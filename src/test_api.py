import unittest
import requests


class APITest(unittest.TestCase):
    URL = "http://127.0.0.1:5000/api/weather/"

    testdata = {
        "Max_temp": -1.7,
        "Min_temp": -9.4,
        "Precipitation": None,
        "Recorded_date": "Wed, 23 Jan 1985 00:00:00 GMT",
        "Station_ID": "USC00110072"
    }

    teststat = {
        "Avg_max_temp": 20.70491,
        "Avg_min_temp": 8.1695,
        "Recorded_year": 2001,
        "Station_ID": "USC00113879",
        "Total_precipitation": 124.22
    }

    # Weatherdata API response
    def test_1_weatherdata_resp(self):
        resp = requests.get(self.URL + '/1')
        self.assertEqual(resp.status_code, 200)
        print("test_1_weatherdata_resp successful")

    # WeatherStat API response
    def test_2_weatherdatastats_resp(self):
        resp = requests.get(self.URL + '/stats/1')
        self.assertEqual(resp.status_code, 200)
        print("test_2_weatherdatastats_resp successful")

    # Weatherdata API pagination
    def test_3_weatherdata_pagination(self):
        resp = requests.get(self.URL + '/12345')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 10)
        print("test_3_weatherdata_pagination successful")

    # WeatherStat API pagination
    def test_4_weatherdatastats_pagination(self):
        resp = requests.get(self.URL + '/stats/387')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 10)
        print("test_4_weatherdatastats_pagination successful")

    # Weatherdata API record check
    def test_5_weatherdata_record(self):
        resp = requests.get(self.URL + '/1?' +
                            'date=1985-01-23&' + 'station_id=USC00110072')
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json()[0], self.testdata)
        print("test_5_weatherdata_record successful")

    # WeatherStat API record check
    def test_6_weatherdatastats_record(self):
        resp = requests.get(self.URL + '/stats/1?' +
                            'year=2001&' + 'station_id=USC00113879')
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json()[0], self.teststat)
        print("test_6_weatherdatastats_record successful")


if __name__ == "__main__":
    unittester = APITest()

    unittester.test_1_weatherdata_resp()
    unittester.test_2_weatherdatastats_resp()
    unittester.test_3_weatherdata_pagination()
    unittester.test_4_weatherdatastats_pagination()
    unittester.test_5_weatherdata_record()
    unittester.test_6_weatherdatastats_record()
