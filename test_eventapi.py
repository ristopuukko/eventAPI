import unittest
import requests
import json
import sys

class TestEventApiRequests(unittest.TestCase):
    # uri_POST = 'http://localhost:5000/event' # DEBUG
    uri_POST = 'http://ec2-34-201-52-248.compute-1.amazonaws.com:5000/event'
    # uri_GET = 'http://localhost:5000/findevent' # DEBUG
    uri_GET = 'http://ec2-34-201-52-248.compute-1.amazonaws.com:5000/findevent'
    def test_event_PASS(self):
        payload = '{"key":"value","another_key":"another_value"}'
        response = requests.post(self.uri_POST, payload)
        self.assertEqual(response.status_code, 200)

    def test_event_FAIL_BAD_JSON(self):
        payload = '{"key":"value","another_key":"badvluea_}'
        response = requests.post(self.uri_POST, payload)
        self.assertEqual(response.status_code, 400)

    def test_findevent_PASS(self):
        payload = {"city":"paris", "st":"2019-01-17:22.57.00", "et":"2019-01-17:22.58.10"}
        response = requests.get(self.uri_GET, payload)
        self.assertEqual(response.status_code, 200)

    def test_findevent_FAIL_BAD_QUERY_STRING(self):
        payload = {"blah":"WAL", "st":"2019-01-17:22.58.00", "et":"2019-01-17:22.58.10"}
        response = requests.get(self.uri_GET, payload)
        self.assertEqual(response.status_code, 400)

    def test_findevent_FAIL_DATA_NOTFOUND(self):
        payload = {"city":"tampere", "st":"2019-01-17:22.58.00", "et":"2019-01-17:22.58.10"}
        response = requests.get(self.uri_GET, payload)
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()