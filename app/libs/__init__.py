from datetime import datetime
from flask import request
import pytz

from app.general import getUtcCurrentTime
from app.libs.flask_ipinfo import IPInfo


def getHostNameAndIp():
    data = {
        "ip": None,
    }
    try:
        ipinfo = IPInfo()
        data["browser"] = ipinfo.browser
        # data['os'] = ipinfo.os
        # data['lang'] = ipinfo.lang
        # data['ipra'] = ipinfo.ipaddress

        if request.environ.get("HTTP_X_FORWARDED_FOR"):
            data["ip"] = request.environ["HTTP_X_FORWARDED_FOR"]
        else:
            data["ip"] = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)

    except Exception as e:
        pass

    return data

def getUserAgents():
    data = {}

    userAgent = request.headers.get("User-Agent")
    # ua = request.user_agent
    # data['ruaPlatform'] = ua.platform
    # data['ruaBrowser'] = ua.browser
    # data['ruaVersion'] = ua.version
    # data['ruaLanguage'] = ua.language
    # data['ruaString'] = ua.language
    if userAgent:
        data["rua"] = userAgent

    if request.headers.get("rurl"):
        data["rurl"] = request.headers.get("rurl")
    # al = request.accept_languages
    # data['ral'] = al

    return data

def getReadableDateFormats(key: str):
    now = getUtcCurrentTime()
    return {key: now}


def getUserSnippet(
    uid: str,
    isNew: bool = False,
    sby: dict = {},
    extra: dict = {},
    updatePrefix="updated",
    createPrefix="created",
    includeUpdatedAt=True,
):
    ip = getHostNameAndIp()
    ua = getUserAgents()

    sessionBy = {}
    if sby:
        if "ut" in sby:
            sessionBy["sut"] = sby["ut"]
        if "fullName" in sby:
            sessionBy["sname"] = sby["fullName"]

    meta = {
        **extra,
        **getReadableDateFormats(f"{updatePrefix}At"),
        f"{updatePrefix}Uid": uid,
        f"{updatePrefix}By": sessionBy,
        f"{updatePrefix}Ip": {**ip, **ua},
    }

    if isNew:
        createdBy = {
            **extra,
            **getReadableDateFormats(f"{createPrefix}At"),
            f"{createPrefix}Uid": uid,
            f"{createPrefix}By": sessionBy,
            f"{createPrefix}Ip": {**ip, **ua},
        }

        if includeUpdatedAt:
            meta = {**createdBy, **meta}
        else:
            meta = createdBy

    return meta
