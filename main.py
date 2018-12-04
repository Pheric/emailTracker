import logging
import os
import db
import siteHandler
import trackerWebHandler
import trackerHandler

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

    # Run the Flask application
    siteHandler.app.run()  # host="0.0.0.0"


if __name__ == "__main__":
    init()
