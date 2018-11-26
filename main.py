import logging
import os
import db
import trackerHandler
import trackerWebHandler

# Tracker links default TTL (one week)
#                                          millis *  s  *   m *   h * d
TRACKER_TTL_MILLIS = (1000 * 60 * 60 * 24 * 7)
DB_FILE_LOCATION = os.path.join(os.path.dirname(__file__), 'emailTrackerDb.sqlite3')


def init():
    """
    Initializes and runs the whole program
    :return: N/A
    """

    # Set log level
    logging.basicConfig(level='DEBUG')

    logging.info("EmailTracker starting up....")

    # Set up the database
    db.init()

    # TESTING
    # Trackers are normally generated when a user wants one made through the website
    print(f"Generate tracker link with UUID: {trackerHandler.generateTracker().tId}")

    # Run the tracker Flask application
    trackerWebHandler.trackerApp.run()


if __name__ == "__main__":
    init()
