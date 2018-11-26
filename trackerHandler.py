import db
from tracker import Tracker

# # List of active tracking links (see Tracker class)
# activeTrackers = []


def generateTracker():
    """
    Generates a Tracker object and inserts it into the db
    :return: the new Tracker object
    """
    tracker = Tracker()

    db.insertTracker(tracker)

    # activeTrackers.append(tracker)
    return tracker


def getTrackerById(id):
    """
    Gets a Tracker object by UUID
    :param id: the UUID of the Tracker to search for
    :return: the Tracker object or None
    """
    # I'm doing this to keep consistency: all calls messing with trackers should be in this file
    return db.selectTrackerById(id)

    # TODO Handle expiring links and deletion of links?

    # millis = utils.current_millis()
    #
    # # Testing
    # print(db.selectTrackerById(id))
    #
    # for t in activeTrackers:
    #     # Automatically remove expired trackers
    #     if millis > t.expiration:
    #         logging.info(f"Removing expired tracker with UUID: {t.tId}")
    #         activeTrackers.remove(t)
    #         continue
    #
    #     # Return current tracker if the Id is correct
    #     if t.tId == id:
    #             return t
    #
    # # Failed to find a tracker with the given Id
    # return None
