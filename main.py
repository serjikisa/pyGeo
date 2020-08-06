"""
main module instanciating a Flask app and this will be our entry point
Views and application hooks also resides in this module, on further development,
will be better to be organized in their own modules.
"""
from flask import Flask
from flask import request, abort, Response
from flask import jsonify
import handlers
from lib import validators
from lib import cache
import settings


app = Flask(__name__)
rediscache = cache.RedisCache(settings.REDIS_HOST, settings.REDIS_PORT)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": e.description}), e.code


@app.before_request
def before_req():
    caller_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    duration = rediscache.get_duration(caller_ip)
    if not duration:
        rediscache.set_time(caller_ip)
    elif duration < settings.CONFIG['REQUEST_INTRVAL']:
        err = {"message": f"Please wait for {settings.CONFIG['REQUEST_INTRVAL'] - duration} seconds"}
        return jsonify(err), 403
    else:
        rediscache.set_time(caller_ip)


@app.route('/')
def root():
    msg = {"message": "Please check the documents how to call one the services: geocode, getloc, geodist"}
    return jsonify(msg), 404


@app.route('/geocode/<string:address>')
def geocode(address):
    return jsonify(handlers.call_service('geocode', address)), 200


@app.route('/geoloc/<string:latlng>')
def geoloc(latlng):
    if not validators.latlng_validate(latlng):
        return jsonify({"message": "Invalid parameters"}), 400

    return jsonify(handlers.call_service('geoloc', latlng)), 200


@app.route('/geodist/<string:latlng1>/<string:latlng2>')
def geodist(latlng1, latlng2):
    if not (validators.latlng_validate(latlng1) and validators.latlng_validate(latlng2)):
        return jsonify({"message": "Invalid parameters"}), 400

    return jsonify(handlers.calculate_distance(latlng1, latlng2)), 200
