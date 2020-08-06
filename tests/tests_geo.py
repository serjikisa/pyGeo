from flask import Flask
import json
from flask_testing import TestCase
from unittest import mock
import main


class ApiTest(TestCase):
    def _get_mock_data(self, name):
        with open(f'data/{name}.json') as f:
            json_resp = json.load(f)
        return json_resp

    def setUp(self):
        self.mock_get_request = mock.patch('handlers._get_request', autospec=True).start()
        self.mock_get_request.return_value = self._get_mock_data('LA')
        self.addCleanup(mock.patch.stopall)

    def create_app(self):
        app = main.app
        app.config['TESTING'] = True
        return app

    def test_geocode_no_arguments(self):
        response = self.client.get('/geocode')
        self.assertEqual(response.status_code, 404)

    def test_geocode_success(self):
        response = self.client.get('/geocode/some address')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_geoloc_bad_argument(self):
        response = self.client.get('/geoloc/250,350')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue('message' in response.json)

    def test_geoloc_success(self):
        response = self.client.get('/geoloc/50,-120')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_geodist_success(self):
        response = self.client.get('/geodist/50,-120/55,-112')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_geodist_noargs(self):
        response = self.client.get('/geodist')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, 'application/json')
        self.assertTrue('message' in response.json)

    def test_geodist_insufficient_args(self):
        response = self.client.get('/geodist/50,-120')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, 'application/json')
        self.assertTrue('message' in response.json)
