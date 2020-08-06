"""
This module provides functions will be called on views endpoints
"""
from lib import geocalc
import requests
import settings


SERVICES = {
    'geocode': 'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}',
    'geoloc':  'https://maps.googleapis.com/maps/api/geocode/json?latlng={0}&key={1}',
}


def _get_request(url):
    """
    Calling external service (Google GeoCode API)
    """
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception('Could not call service')

    return resp.json()


def call_service(service, param):
    """
    Will response to /geocode and /geoloc endpoints
    Process is quite simillar
    """
    if service not in SERVICES.keys():
        raise ValueError('Please provide proper service name')

    url = SERVICES[service].format(param, settings.GOOGLE_API_KEY)
    json_resp = _get_request(url)
    if len(json_resp['results']) == 0:
        return {"error": json_resp['status']}
    else:
        return {
            'address': json_resp['results'][0]['formatted_address'],
            'location': json_resp['results'][0]['geometry']['location']
        }


def calculate_distance(latlng1, latlng2):
    """
    Will be called on /geodist endpoint
    Is using geocalc.distance implemented library
    """
    point1 = [float(item) for item in latlng1.split(',')]
    point2 = [float(item) for item in latlng2.split(',')]
    dist = geocalc.distance(point1, point2)
    return {"distnace(km)": dist}
