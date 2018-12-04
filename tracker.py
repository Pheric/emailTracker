import logging
from uuid import uuid4

import db
import main
from utils import current_millis


class Tracker:
    """Class to store information about any one tracking link"""

    def __init__(self, desc):
        self.tId = uuid4()
        self.expiration = current_millis() + main.TRACKER_TTL_MILLIS
        self.desc = desc

    def registerHit(self, clientIp):
        """
        Method called automatically when the Tracker link is hit. Inserts a hit in the database automatically.
        :param clientIp: IP address of the client
        :return: N/A
        """
        logging.debug(f"Tracker with UUID {self.tId} registered hit, inserting into db")

        db.insertHit(self, clientIp)
