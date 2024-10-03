from datetime import timedelta

import pytz

# User App Version history
G_APP_VERSION_NUMBER = 1.0
G_APP_MIN_VERSION_NUMBER = 1
G_CURRENT_APP_VERSION = 1
G_UP_APP_VERSION_NAME = ""

#
G_MIDDLE_DOT = " • "
G_RUPEE_SYMBOL = "₹ "

G_SELECT_INDIA_COUNTRY = {
    "key": "C001",
    "label": "INDIA",
}

G_ACCESS_EXPIRES = timedelta(minutes=50000000)
G_REFRESH_EXPIRES = timedelta(days=30)
G_TIME_DIFFERENCE_IST_SECONDS = 19800  # 5 hrs 30 mins in seconds
G_ONE_DAY_IN_SECONDS = 86400


G_DATE_FORMAT = "%d/%m/%Y"
G_DATE_FORMAT_V1 = "%d-%m-%Y"
G_DT_FORMAT = "%d/%m/%Y %I:%M %p"
G_MONTH_YEAR_FORMAT = "%m/%Y"
G_TIME_FORMAT = "%H:%M:%S"
G_DATETIME_FORMAT = f"{G_DATE_FORMAT} {G_TIME_FORMAT}"
G_DATETIME_FORMAT_V1 = f"{G_DATE_FORMAT_V1} {G_TIME_FORMAT}"
G_DATE_FORMAT_REVERSE = "%Y/%m/%d"
G_DAY_FORMAT = "%d"
G_MONTH_FORMAT_READABLE = "%B"
G_YEAR_FORMAT = "%Y"
G_DATE_FORMAT_REVERSE_HYPHIN = "%Y-%m-%d"
G_DATE_FORMAT_REVERSE_HYPHIN_V1 = "%Y-%m-%d %H:%M:%S.%f"
G_DATE_FORMAT_REVERSE_HYPHIN_V2 = "%Y-%m-%d %H:%M:%S"
G_DT_REV_HYP_V2 = "%Y-%m-%dT%H:%M:%S"
G_DT_REV_HYP_V3 = "%Y-%m-%dT%H:%M:%S.%fZ"
G_DT_REV_HYP_V4 = "%Y-%m-%dT%H:%M"
G_OPENPYXL_DATE_FORMAT = "DD/MM/YYYY"
G_OPENPYXL_DATETIME_FORMAT = "DD/MM/YYYY hh:mm:ss AM/PM"
G_DATETIME_FORMAT_REVERSE = "%Y-%m-%d %H:%M:%S"
G_DATE_FORMAT_IN_DOT = "%d.%m.%Y"
G_DATE_FORMAT_READABLE = "%d %b, %Y"
G_DATE_FORMAT_FULLNAME_READABLE = "%d %B, %Y (%A)"
G_SHORT_MONTH_YEAR_FORMAT_READABLE = "%b, %Y"
G_MONTH_YEAR_FORMAT_READABLE = "%B, %Y"
G_DATE_TIME_DOWNLOAD_PATH_SUFFIX = "%Y_%m_%d_%H_%M_%S"
G_DATETIME_12HR_FORMAT = f"{G_DATE_FORMAT} %H:%M %p"
G_DATETIME_FORMAT_READABLE = f"{G_DATE_FORMAT_READABLE} %I:%M %p"
G_DATETIME_SECONDS_FORMAT = "%d-%m-%Y %H:%M:%S"

G_BILLDESK_DATE_TIME = "%Y%m%d%H%M%S"

G_SHORT_MONTH_YEAR_FORMAT_READABLE_IN_SLASH = "%b/%Y"
G_PDF_DATE_FORMAT = "%d.%m.%Y"
G_PDF_DATETIME_FORMAT = f"{G_PDF_DATE_FORMAT} %I:%M %p"
G_PDF_MONTH_YEAR_FORMAT = "%m.%Y"
G_INDIAN_TIMEZONE = pytz.timezone("Asia/Kolkata")


G_DAY_NAMES = [
    "Zero",
    "First",
    "Second",
    "Third",
    "Fourth",
    "Fiveth",
    "Sixth",
    "Seventh",
    "Eighth",
    "Nineth",
    "Tenth",
    "Eleventh",
    "Twelveth",
    "Thirteenth",
    "Fourteenth",
    "Fifteenth",
    "Sixteenth",
    "Seventeenth",
    "Eighteenth",
    "Nineteenth",
    "Twentieth",
    "Twenty First",
    "Twenty Second",
    "Twenty Third",
    "Twenty Fourth",
    "Twenty Fifth",
    "Twenty Sixth",
    "Twenty Seventh",
    "Twenty Eighth",
    "Twenty Nineth",
    "Thirtieth",
    "Thirty First",
]

commonError = {"status": 0, "class": "error", "message": "Error", "payload": {}}
G_SCHEDULE_TYPE = ["scheduleOn", "scheduleNow"]

G_FRONT_END_FORMATS = {
    G_DATE_FORMAT: "DD/MM/YYYY",
    G_MONTH_YEAR_FORMAT: "MM/YYYY",
    G_TIME_FORMAT: "HH:MM:SS",
    G_DATETIME_FORMAT: "DD/MM/YYYY HH:MM:SS",
    G_DATE_FORMAT_REVERSE: "YYYY/MM/DD",
    G_YEAR_FORMAT: "YYYY",
    G_DATE_FORMAT_REVERSE_HYPHIN: "YYYY-MM-DD",
    G_OPENPYXL_DATE_FORMAT: "DD/MM/YYYY",
    G_OPENPYXL_DATETIME_FORMAT: "DD/MM/YYYY hh:mm:ss AM/PM",
    G_DATETIME_FORMAT_REVERSE: "YYYY-MM-DD HH:MM:SS",
    G_DATE_FORMAT_IN_DOT: "DD.MM.YYYY",
    G_DATE_FORMAT_READABLE: "DD MMM, YYYY",
    G_SHORT_MONTH_YEAR_FORMAT_READABLE: "MMM, YYYY",
    G_MONTH_YEAR_FORMAT_READABLE: "MMMM, YYYY",
    G_DATE_TIME_DOWNLOAD_PATH_SUFFIX: "YYYY_MM_DD_HH_MM_SS",
}


G_CLIENT_KEYS = ["sa", "a", "ih", "is", "ad"]
G_FH_PREFIX = ["D/O", "W/O", "S/O", "C/O"]
G_YES_NO = ["Yes", "No"]
G_NAME_TITLES = ["Mr", "Ms", "Mrs", "Miss", "Tr", "Mx"]


G_CLIENT_TYPE_LABELS = {
    "sa": {"label": "Super Admin", "key": "SA"},
    "a": {"label": "Admin", "key": "A"},
    "pu": {"label": "Public", "key": "PU"},
}

G_DB_LIST_CATEGORIES = {
    "district": "listDistricts",
    "aboutus": "about"}
