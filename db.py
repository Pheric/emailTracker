import sqlite3
import uuid
import main
from sqlite3 import Error
import logging
import tracker


def insertTracker(t):
    """
    Inserts a Tracker object into the sqlite database
    :param t: the Tracker to insert
    :return: N/A
    """
    try:
        logging.debug(f"Inserting tracker with UUID {t.tId} into db")
        execute("INSERT INTO Trackers (id, expirationTime) VALUES (?, ?);", str(t.tId), t.expiration)
    except Error as e:
        logging.error(f"Error while inserting tracker with UUID {t.tId}:\n{e}")


def selectTrackerById(id):
    """
    Tries to fetch a specific Tracker from the db
    :param id: the UUID of the Tracker to look for
    :return: The appropriate Tracker object or None
    """
    try:
        with sqlite3.connect(main.DB_FILE_LOCATION) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM Trackers WHERE id = ?;", (str(id),))
            rows = c.fetchall()

            if len(rows) == 0:
                return None

            t = tracker.Tracker()
            # Indexes should be safe as columns are guaranteed NOT NULL, see table definition below
            t.tId = (uuid.UUID(rows[0][0]))
            t.expiration = (int(rows[0][1]))

            return t
    except Error as e:
        logging.error(f"Error selecting all trackers from DB:\n{e}")


def insertHit(t, ipAddr):
    """
    Inserts a hit into the db
    :param t: the Tracker that was hit
    :param ipAddr: the ip address of the client that hit the link
    :return: N/A
    """
    execute("INSERT OR IGNORE INTO Hits (trackerId, ipAddr) VALUES (?, ?);", str(t.tId), ipAddr)


#                  varargs   v
def execute(stmt, *params):
    """
    Execute a SQL statement on the internal sqlite3 db
    Throws a sqlite3 Error object
    :param stmt: the statement to execute
    :param params: additional sql parameters
    :return: N/A
    """
    with sqlite3.connect(main.DB_FILE_LOCATION) as conn:
        c = conn.cursor()
        c.execute(stmt, params)


def init():
    """
    Sets up the sqlite3 db
    :return: N/A
    """
    logging.info(f"Setting up the sqlite3 database in {main.DB_FILE_LOCATION} ...")

    createTrackersTbl =\
        """
        CREATE TABLE IF NOT EXISTS Trackers (
            id NCHAR(36) PRIMARY KEY,
            expirationTime INTEGER NOT NULL
        );
        """

    createHitsTbl =\
        """
        CREATE TABLE IF NOT EXISTS Hits (
            id INTEGER PRIMARY KEY, /* autoincrementing */
            trackerId NCHAR(36) NOT NULL, /* FK */
            reqTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            ipAddr VARCHAR(15),
            FOREIGN KEY (trackerId) REFERENCES Trackers(id)
        );
        """

    try:
        execute(createTrackersTbl)
        execute(createHitsTbl)
    except Error as e:
        logging.error(f"Error while creating database tables:\n{e}")

    logging.info("Finished setting up the database!")
