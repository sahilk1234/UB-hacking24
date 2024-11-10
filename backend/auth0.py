from functools import wraps
from flask import session, redirect, url_for
from authlib.integrations.flask_client import OAuth
from os import environ as env
from dotenv import find_dotenv, load_dotenv

oauth = OAuth()
auth0 = None  # Placeholder for the global auth0 instance

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

def init_auth0(app):
    """Initialize Auth0 with the Flask app."""
    global auth0  # Ensure auth0 is a global variable so it can be accessed in app.py
    oauth.init_app(app)
    auth0 = oauth.register(
        "auth0",
        client_id=env.get("AUTH0_CLIENT_ID"),
        client_secret=env.get("AUTH0_CLIENT_SECRET"),
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)
    return auth0

def auth_required(f):
    """Decorator to ensure user authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated
