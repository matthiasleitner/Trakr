import sqlite3

from config import ConfigHelper
from file.pcap import Observation
from database import PrivacyUtility

create_reduced_db = "CREATE TABLE IF NOT EXISTS %s \
               (ID INT PRIMARY KEY     NOT NULL, \
               ADDRESS         TEXT    NOT NULL, \
               TIME            DOUBLE  NOT NULL, \
               TYPE            SHORT   NOT NULL, \
               LAT             DOUBLE  NOT NULL, \
               LONG            DOUBLE  NOT NULL);"
create_behavior_db = "CREATE TABLE IF NOT EXISTS %s\
               (ADDRESS   TEXT   PRIMARY KEY   NOT NULL);"
create_usercount_db = "CREATE TABLE IF NOT EXISTS %s" \
                      "(TIME    DOUBLE  NOT NULL," \
                      "NUM_USERS    INT     NOT NULL)"

get_all_macs = "SELECT ADDRESS FROM %s"
insert_command = "INSERT INTO %s (ADDRESS) VALUES ('%s')"


def init():
    conn = connect()
    __behavioralDatabaseInit(conn)


def loadObservation(connection, mac, time, type):
    # TODO:adds in the data to the table

    return


def connect():
    pathToDB = ConfigHelper.getBehaviorDatabasePath()
    connection = sqlite3.connect(pathToDB)
    return connection


def commit(connection):
    connection.commit()


def close(connection):
    connection.close()


# this makes the database if it does not exist
def __behavioralDatabaseInit(connection):
    # makign table to hold how many users are currently present for an interval
    connection.execute(create_usercount_db % ConfigHelper.getUserCountTableName())
    # making table to hold all unique MACs
    connection.execute(create_behavior_db % ConfigHelper.getUniqueTableName())
    # making table for the behaviors of when they enter and exit
    connection.execute(create_reduced_db % ConfigHelper.getReducedTableName())

    # adding in the default MACs that are not needed
    __addPresetAddresses(connection)

    connection.commit()


def __addPresetAddresses(connection):
    for addr in Observation.bad_addresses:
        addNewAddress(connection, addr)
    return


# True - if the address was successfully stored or it was ignored
# False - if there was a problem storing the address
def addNewAddress(connection, address):
    try:
        address = PrivacyUtility.processAddress(address)
        connection.execute(insert_command % (str(ConfigHelper.getUniqueTableName()), address))
        connection.commit()
    except Exception, errmsg:
        # print "New MAC address not inserted, was not unique"
        # print errmsg
        # I'll just let it handle uniqueness checking, maybe fix this if it gets slow
        return False
    return True


def getUniques(connection):
    cursor = connection.execute(get_all_macs % str(ConfigHelper.getUniqueTableName()))
    macs = []
    for c in cursor:
        macs.append(c[0])

    return macs
