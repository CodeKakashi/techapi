from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.integrations.whatsapp import Whatsapp
from app.config import Config

from app.settings import JWT_SECRET_KEY
# from apscheduler.schedulers.background import BackgroundScheduler

def create_app():
    app = Flask(__name__)
    # scheduler = BackgroundScheduler()
    app.debug = True
    app.config.from_object(Config)
    CORS(app)

    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    jwt = JWTManager(app)

    from app.authLogin import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/server/api")

    from app.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix="/server/api")

    from app.integrations import integrations_bp
    app.register_blueprint(integrations_bp, url_prefix="/server/api")

    from app.dev import dev_bp
    app.register_blueprint(dev_bp, url_prefix="/server/api")

    from app.loans import loans_bp
    app.register_blueprint(loans_bp, url_prefix="/server/api")
    
    # my_cron_job = Whatsapp()
    # scheduler.add_job(func=my_cron_job.sendSMS, trigger='interval', minutes=5)
    # scheduler.start()

    return app
