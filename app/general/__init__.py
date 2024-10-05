from datetime import datetime
import string
import bcrypt
from flask import request
import pytz
from app.config import PROD_MONGO_DATABASE, PROD_MONGO_URI
import pymongo
from random import choice
import calendar
from flask_bcrypt import Bcrypt


client = pymongo.MongoClient(PROD_MONGO_URI)
mdb = client[PROD_MONGO_DATABASE]

# Function to hash the password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def numGenerator(size=6, chars=string.digits):
    return "".join(choice(chars) for x in range(size))


def getUtcCurrentTime():
    return datetime.now(tz=pytz.UTC)

def timestamp(byTimezone=False):
    d = getUtcCurrentTime()

    ct = calendar.timegm(d.utctimetuple())

    return ct


def alphaNumGenerator(size=4, chars="ABCDEFGHJKLMNPQRSTUVWYZ123456789"):
    return "".join(choice(chars) for x in range(size))

def uniqueId(digit=4, isNum=False, ref={}, prefix=None, suffix=None):
    _id = numGenerator(digit) if isNum else alphaNumGenerator(digit)

    if prefix is not None:
        _id = f"{prefix}{_id}"

    if suffix is not None:
        _id = f"{_id}{suffix}"

    mUniqueIds = mdb.uuid
    data = mUniqueIds.find_one({"_id": _id})

    if data and "_id" in data:
        return uniqueId(digit, isNum, ref, prefix, suffix)
    else:
        userId = _id.upper()
        mUniqueIds.insert_one({"_id": userId, **ref})
        return userId
    
def verifyPassword(bcryptPasswordHash, password):
    return Bcrypt().check_password_hash(bcryptPasswordHash, password)
    
def safelyConvertToInt(str):
    try:
        return int(float(str))
    except ValueError:
        return str
    
def cleanupEmail(value, ifEmpty=""):
    if not value:
        return ifEmpty

    return cleanupValue(value, returnType="string").lower()
    
def cleanupValue(value, returnType="string", ifEmpty=None):
    if returnType == "list":
        return value

    if not value:
        return ifEmpty

    value = str(value).strip()

    if value == "":
        return ifEmpty

    if returnType == "int":
        return safelyConvertToInt(value)
    elif returnType == "bool":
        value = value[:1].lower()
        return True if value in {"y", "t"} else False

    return value

def uniqueSerialNumber(type, filter=None, params=None, targetCollection = "usno"):
    if not filter:
        filter = {}

    if not params:
        params = {}

    type = type.upper()
    while 1:
        cursor = (
            mdb[targetCollection]
            .find({"_type": type, **filter}, {"_id": 1, "_i": 1})
            .sort([("_i", -1)])
        )

        seq = 1
        if "seq" in params:
            seq = int(params["seq"])
        try:
            record = cursor.next()

            seq = record["_i"] + 1
        except StopIteration:
            # print("Empty No Sequence yet!")
            pass

        _id = f"{type}X{seq}"

        if "year" in filter:
            _id = f"{type}X{filter['year']}X{seq}"

        if "uid" in filter:
            _id = f"{type}X{filter['uid']}X{seq}"

        if "rid" in filter:
            _id = f"{type}X{filter['rid']}X{seq}"

        if "dqid" in filter:
            _id = f"{type}X{filter['dqid']}X{seq}"

        doc = {**params, **filter, "_id": _id, "_type": type, "_i": seq}
        try:
            results = mdb[targetCollection].insert_one(doc)
        except pymongo.errors.DuplicateKeyError:
            # skip document because it already exists in new collection
            continue
        break

    return seq

def getDayStart(dt):
    if isinstance(dt, datetime):
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    
def getDayEnd(dt):
    if isinstance(dt, datetime):
        return dt.replace(hour=23, minute=59, second=59, microsecond=999999)
    
def convertDateToCustomFormat(date_str):
    if date_str.endswith('Z'):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%fZ')
    else:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
    
    # Format the datetime object into the desired string format
    formatted_date = date_obj.strftime('%d/%m/%Y %I:%M %p')
    
    return formatted_date

