from core.api import utils
from core.api.api_cardpay_app import cardpay_app
from core.api.api_crons_app import crons_app
from core.api.api_pg import pg
from core.api.api_retool_app import retool as retool_app
from core.api.api_rp import rp_app
from core.api.api_vendor_app import vendor_app
from flask import Flask

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
app.register_blueprint(rp_app)


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
