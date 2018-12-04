import logging
from flask import send_file, request, redirect
import siteHandler
import trackerHandler


@siteHandler.app.route("/t/<uuid:trackerId>", methods=['GET'])
@siteHandler.app.route("/t/<uuid:trackerId>/", methods=['GET'])
@siteHandler.app.route("/t/<uuid:trackerId>/<path:path>", methods=['GET'])
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


@siteHandler.app.route("/generate", methods=["POST"])
def genLink():
    """
    Called by Flask when a client generates a new link
    :return: the id for the tracker link
    """
    if not siteHandler.checkAuthed(request):
        return redirect('/login')
    if 'desc' not in request.form:
        return redirect("/view")
    # return ignored   v
    trackerHandler.generateTracker(request.cookies['username'], request.form['desc'])
    return redirect("/view")
