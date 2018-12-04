import db
from tracker import Tracker

# # List of active tracking links (see Tracker class)
# activeTrackers = []


# https://xkcd.com/1987/
def generateTracker(user, description):
    """
    Generates a Tracker object and inserts it into the db
    :param user: Username of user generating the Tracker
    :param description: Description of the tracker link
    :return: the new Tracker object
    """
    tracker = Tracker(description)

    db.insertTracker(tracker, user)

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
