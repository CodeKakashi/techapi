from . import integrations_api

from app.integrations.whatsapp import Whatsapp
integrations_api.add_resource(Whatsapp, "/whatsapp")