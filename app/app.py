import os
from flask import Flask, render_template
from . import controllers, models, setting,admindashboard
from .extensions import db, json, scheduler, ma, rq, basic_auth
from flask.cli import with_appcontext
from . import schedular
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
from flask_cors import CORS
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import rq_dashboard
from datetime import timedelta

project_dir = os.path.dirname(os.path.abspath(__file__))

def create_app(config_object=setting):
    sentry_sdk.init(
        dsn=setting.SENTRY_URL,
        integrations=[FlaskIntegration()]
    )
    app = Flask(__name__)
    app.config.from_object(config_object)
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler('flask.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    register_extensions(app)
    register_blueprints(app)
    register_admin(app)
    # register_errorhandlers(app)
    register_schedular(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    json.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)
    ma.init_app(app)
    rq.init_app(app)
    basic_auth.init_app(app)
    # default_worker = rq.get_worker()
    # default_worker.work(burst=True)
    # scheduler = rq.get_scheduler(interval=60)
    # scheduler.run()
    CORS(app, supports_credentials=True)
    with app.app_context():
        db.create_all() 
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(controllers.dam.blueprint)
    app.register_blueprint(controllers.forecast.blueprint)
    app.register_blueprint(controllers.auth.blueprint)
    app.register_blueprint(controllers.notification.blueprint)
    app.register_blueprint(controllers.staff.blueprint)
    app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")
    return None


def register_admin(app):
    """Register admin pannel"""
    admin = Admin(app, name='Flood', template_mode='bootstrap3',index_view=admindashboard.MyAdminIndexView())
    from .models.values import Values
    from .models.dam import Dam
    from .models.user import User
    from .models.iot import Iot
    from .models.forecast import Forecast
    from .models.subscribe import Subscribe
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Dam, db.session))
    admin.add_view(ModelView(Iot, db.session))
    admin.add_view(ModelView(Subscribe, db.session))
    admin.add_view(ModelView(Values, db.session))
    


def register_schedular(app):
    '''register schedulars of application'''
    controllers.notification.add.cron('* * * * *', 'add',1,2)
    controllers.notification.send_mails.cron('7 * * * *', 'send_mail')
    controllers.notification.send_tweet.cron('9 * * * *', 'send_tweet')
    controllers.dam.fetch_dams.cron('0 * * * *', 'fetch')
    controllers.forecast.forecast_values.cron('5 * * * *', 'store_forecast')


# def register_errorhandlers(app):
#     """Register error handlers."""
#     @app.errorhandler(401)
#     def internal_error(error):
#         return render_template('401.html'), 401

#     @app.errorhandler(404)
#     def page_not_found(error):
#         return render_template('404.html'), 404

#     @app.errorhandler(500)
#     def internal_error(error):
#         return render_template('500.html'), 500

#     return None

