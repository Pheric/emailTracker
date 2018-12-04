import sqlite3
import uuid

import hit
import main
from sqlite3 import Error
import logging
import tracker
import utils


def checkAcct(username, password):
    logging.info(f"Checking account with username {username}")
    try:
        with sqlite3.connect(main.DB_FILE_LOCATION) as conn:
            c = conn.cursor()
            c.execute("SELECT  secret, salt FROM Accts WHERE id = ?;", (username,))
            rows = c.fetchall()

            return (len(rows) != 0) and (utils.checkHash(rows[0][0], password + rows[0][1]))
    except Error as e:
        logging.error(f"Error checking password for user {username}: \n{e}")
        return False


def acctExists(username):
    try:
        with sqlite3.connect(main.DB_FILE_LOCATION) as conn:
            c = conn.cursor()
            c.execute("SELECT  id FROM Accts WHERE id = ?;", (username,))
            rows = c.fetchall()

            return len(rows) != 0
    except Error as e:
        logging.error(f"Error checking if user {username} exists: \n{e}")
        return True


def insertAcct(acct):
    """
    Inserts a new account into the db
    :param acct: the Account to insert
    :return:  OK (T/F)
    """
    if acctExists(acct.id):
        return False
    try:
        logging.debug(f"Inserting new account with username/id {acct.id} into db")
        execute("INSERT INTO Accts (id, secret, salt, email) VALUES (?, ?, ?, ?);", acct.id, acct.secret, acct.salt, acct.email)
        return True
    except Error as e:
        logging.error(f"Error while inserting new account with username/id: {acct.id}:\n{e}")
        return False


def insertTracker(t, username):
    """
    Inserts a Tracker object into the sqlite database
    :param t: the Tracker to insert
    :param username: Username of the user generating the link
    :return: N/A
    """
    try:
        logging.debug(f"Inserting tracker with UUID {t.tId} into db")
        execute("INSERT INTO Trackers (id, expirationTime, userId, description) VALUES (?, ?, ?, ?);", str(t.tId), t.expiration, username, t.desc)
    except Error as e:
        logging.error(f"Error while inserting tracker with UUID {t.tId}:\n{e}")


def selectUserTrackers(username):
    trackers = []
    try:
        with sqlite3.connect(main.DB_FILE_LOCATION) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM Trackers WHERE userId = ?;", (username,))
            rows = c.fetchall()

            if len(rows) == 0:
                return None

            for r in rows:
                # Indexes should be safe as columns are guaranteed NOT NULL, see table definition below
                t = tracker.Tracker(r[3])
                t.tId = (uuid.UUID(r[0]))
                t.expiration = (int(r[1]))
                trackers.append(t)

            return trackers
    except Error as e:
        logging.error(f"Error selecting all trackers from DB:\n{e}")
        return trackers


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

            t = tracker.Tracker(rows[0][3])
            # Indexes should be safe as columns are guaranteed NOT NULL, see table definition below
            t.tId = (uuid.UUID(rows[0][0]))
            t.expiration = (int(rows[0][1]))

            return t
    except Error as e:
        logging.error(f"Error selecting all trackers from DB:\n{e}")
        return None


def selectHits(trackerId, userId):
    try:
        with sqlite3.connect(main.DB_FILE_LOCATION) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM Hits WHERE trackerId = ? AND (SELECT userId from Trackers WHERE id = ? ) = ? LIMIT 15;", (str(trackerId), str(trackerId), userId))
            rows = c.fetchall()

            if len(rows) == 0:
                return None

            hits = []
            for r in rows:
                hits.append(hit.DisplayHit(r[1], r[2], r[3]))

            return hits
    except Error as e:
        logging.error(f"Error selecting all trackers from DB:\n{e}")
        return None


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
            expirationTime INTEGER NOT NULL,
            userId VARCHAR(16),
            description VARCHAR(256),
            FOREIGN KEY (userId) REFERENCES Accts(id)
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

    createAcctsTbl =\
        """
        CREATE TABLE IF NOT EXISTS Accts (
            id VARCHAR(16) PRIMARY KEY,
            creationTime TIMESTAMP NOT NULL DEFAULT  CURRENT_TIMESTAMP,
            secret VARCHAR(256) NOT NULL DEFAULT 'hunter2',
            salt VARCHAR(128) NOT NULL,
            email VARCHAR(64)
        );
        """

    try:
        execute(createTrackersTbl)
        execute(createHitsTbl)
        execute(createAcctsTbl)
    except Error as e:
        logging.error(f"Error while creating database tables:\n{e}")

    logging.info("Finished setting up the database!")
