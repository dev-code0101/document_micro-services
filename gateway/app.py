# gateway/app.py

from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Rule
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.wrappers import Request, Response
import requests

app = Flask(__name__)

# Define routes to forward requests to corresponding microservices
app.url_map.add(Rule("/auth/", endpoint="auth"))
app.url_map.add(Rule("/artifact/", endpoint="artifact"))
app.url_map.add(Rule("/document/", endpoint="document"))

# Microservice URLs
auth_service_url = "http://localhost:5001"
artifact_service_url = "http://localhost:5002"
document_service_url = "http://localhost:5003"

# ProxyFix middleware to handle reverse proxy headers
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.endpoint("auth")
def auth():
    url = f"{auth_service_url}{request.full_path}"
    response = requests.request(method=request.method, url=url, json=request.get_json())
    return Response(
        response.content, status=response.status_code, headers=response.headers
    )


@app.endpoint("artifact")
def artifact():
    url = f"{artifact_service_url}{request.full_path}"
    response = requests.request(method=request.method, url=url, json=request.get_json())
    return Response(
        response.content, status=response.status_code, headers=response.headers
    )


@app.endpoint("document")
def document():
    url = f"{document_service_url}{request.full_path}"
    response = requests.request(method=request.method, url=url, json=request.get_json())
    return Response(
        response.content, status=response.status_code, headers=response.headers
    )


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = jsonify({"error": e.description})
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    app.run(debug=True)
