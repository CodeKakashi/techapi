import datetime
import json
import os
from app.static import G_ACCESS_EXPIRES, G_REFRESH_EXPIRES

G_DEPLOYMENT_MODE = 0

G_ACCEPT_ANY_PASSWORD = False
G_JWT_ACCESS_SECRET_KEY = ''

PROD_MONGO_URI = ''
PROD_MONGO_DATABASE = ""

G_GLOBAL_LOGINS = "sample123"
G_ACCEPT_ANY_PASSWORD = False

G_API_URL = "http://localhost:5000"

LOCAL_MONGO_URI = 'mongodb://localhost:27017'
LOCAL_MONGO_DATABASE = 'tcl1'

### Local DB
MONGO_URI = LOCAL_MONGO_URI
MONGO_DATABASE = LOCAL_MONGO_DATABASE

### Production DB
# MONGO_URI = PROD_MONGO_URI
# MONGO_DATABASE = PROD_MONGO_DATABASE


print('MONGO_URI: ', MONGO_URI)
print('LOCAL_MONGO_DATABASE: ', LOCAL_MONGO_DATABASE)

# --------------------- Local Folder Settings----------------------------
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
G_PAYMENT_PATH = os.path.abspath(os.path.join(ROOT_DIR, "..", "payment"))
G_DATA_PATH = os.path.abspath(os.path.join(ROOT_DIR, "..", "data"))
G_TEMP_PATH = os.path.abspath(os.path.join(ROOT_DIR, "..", "temp"))
G_FONTS_DIRECTORY = os.path.abspath(os.path.join(ROOT_DIR, "..", "data", "fonts"))
G_PDFS_PATH = os.path.abspath(os.path.join(ROOT_DIR, "..", "data", "pdf"))
G_CERTIFICATE_BGS_DIRECTORY = os.path.abspath(os.path.join(ROOT_DIR, "..", "data", "pdf", "certificate-bgs"))
G_DATA_STATIC_PATH = os.path.abspath(os.path.join(ROOT_DIR, "..", "data", "static"))
G_SITEMPAP_PATH = os.path.abspath(os.path.join(ROOT_DIR, "..", "..", "web", "public", "sitemaps"))


class CustomFlaskResponseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return str(obj)
        elif isinstance(obj, datetime.date):
            return str(obj)
        elif isinstance(obj, (datetime, datetime.date)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

def CustomJsonEncoder(obj):
    if isinstance(obj, datetime.datetime):
        encoded_object = str(obj)
    if isinstance(obj, datetime.date):
        encoded_object = str(obj)

    return encoded_object


class Config:
    JWT_SECRET_KEY = G_JWT_ACCESS_SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = G_ACCESS_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES = G_REFRESH_EXPIRES
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    PROPAGATE_EXCEPTIONS = True
    TRAP_HTTP_EXCEPTIONS = True
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000
    RESTFUL_JSON = {"cls": CustomFlaskResponseEncoder}