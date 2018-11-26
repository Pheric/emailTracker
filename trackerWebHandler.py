import logging

from flask import Flask, send_file, request

import trackerHandler

trackerApp = Flask(__name__)


@trackerApp.route("/t/<uuid:trackerId>", methods=['GET'])
@trackerApp.route("/t/<uuid:trackerId>/<path:path>", methods=['GET'])
def trackerGet(trackerId, path=None):
    """
    Called by Flask when a client requests a Tracker link or similar
    :param trackerId: the UUID of the tracker
    :param path: an ignored variable that lets Flask ignore everything after the UUID in the URL
    :return: Sends a 1x1 pixel PNG to the client
    """
    tracker = trackerHandler.getTrackerById(trackerId)
    if tracker is not None:
        logging.info(f"Hit on tracker with UUID: {trackerId} from IP: {request.remote_addr}")
        tracker.registerHit(request.remote_addr)
    else:
        logging.debug(f"Hit on NONEXISTENT tracker with UUID: {trackerId}")

    return send_file('static/pixel.png', mimetype='image/png')
