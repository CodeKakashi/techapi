from app.dev.static import GenerateStatic
from . import dev_api

dev_api.add_resource(GenerateStatic, "/generate/static")