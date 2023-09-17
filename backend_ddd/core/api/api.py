# from dataclasses import asdict

import firebase_admin
import os
import sentry_sdk

from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask

from core.api import utils
from core.api.api_vendor_app import vendor_app
from core.api.api_cardpay_app import cardpay_app
from core.api.api_retool_app import retool as retool_app
from core.api.api_pg import pg

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

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True

app.register_blueprint(cardpay_app)
app.register_blueprint(retool_app)
app.register_blueprint(vendor_app)
app.register_blueprint(pg)

cred = firebase_admin.credentials.Certificate("core/api/credentials-prod.json")
firebase_admin.initialize_app(cred)

# 200 OK
# The request succeeded. The result meaning of "success" depends on the HTTP method:

# 201 Created
# The request succeeded, and a new resource was created as a result.
# This is typically the response sent after POST requests, or some PUT requests.

# 400 Bad Request
# The server cannot or will not process the request due to something
# that is perceived to be a client error (e.g., malformed request syntax,
# invalid request message framing, or deceptive request routing).

# 401 Unauthorized
# Although the HTTP standard specifies "unauthorized", semantically this response means
# "unauthenticated". That is, the client must authenticate itself to get the requested response.

# 404 Not Found
# The server cannot find the requested resource. In the browser, this means the URL is
# not recognized. In an API, this can also mean that the endpoint is valid but the resource
# itself does not exist. Servers may also send this response instead of 403 Forbidden to hide
# the existence of a resource from an unauthorized client. This response code is probably the most
# well known due to its frequent occurrence on the web.

# 500 Internal Server Error
# The server has encountered a situation it does not know how to handle.

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
