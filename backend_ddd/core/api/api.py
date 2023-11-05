# from dataclasses import asdict

import os

import firebase_admin
import google.cloud.logging
import sentry_sdk
from core.api import utils
from core.api.api_cardpay_app import cardpay_app
from core.api.api_crons_app import crons_app
from core.api.api_pg import pg
from core.api.api_retool_app import retool as retool_app
from core.api.api_vendor_app import vendor_app
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

""" 
    --- --- --- --- --- --- --- --- --- --- --- ---
    Sentry setup
    --- --- --- --- --- --- --- --- --- --- --- ---
"""
sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[
        FlaskIntegration(),
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)

"""
    --- --- --- --- --- --- --- --- --- --- --- ---
    Google cloud logging setup
    --- --- --- --- --- --- --- --- --- --- --- ---
"""

# Instantiates a client
client = google.cloud.logging.Client()

# # Retrieves a Cloud Logging handler based on the environment
# # you're running in and integrates the handler with the
# # Python logging module. By default this captures all logs
# # at INFO level and higher
client.setup_logging()

"""
    --- --- --- --- --- --- --- --- --- --- --- ---
    Flask app setup
    --- --- --- --- --- --- --- --- --- --- --- ---
"""

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True

app.register_blueprint(cardpay_app)
app.register_blueprint(retool_app)
app.register_blueprint(vendor_app)
app.register_blueprint(pg)
app.register_blueprint(crons_app)

cred = firebase_admin.credentials.Certificate("core/api/credentials-prod.json")
firebase_admin.initialize_app(cred)

PREFIX = "/api/v1"


@app.route(PREFIX)
def base():
    """base endpoint"""

    return utils.Response(message="Welcome to the backend", status_code=200).__dict__


@app.errorhandler(utils.CustomException)
def handle_exceptions(e: utils.CustomException):
    payload = {
        "message": e.message,
        "event_code": e.event_code.name,
    }
    return payload, e.status_code
