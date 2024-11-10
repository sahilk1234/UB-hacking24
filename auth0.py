from functools import wraps
from flask import session, redirect, url_for
from authlib.integrations.flask_client import OAuth

auth0 = OAuth().register(
    'auth0',
    client_id='CrpFtQ74X9XVp3EE7A5pHQYNS6HNbISF',
    client_secret='cXC_JXEBFVcoAgIxrsc0t8X3snfdslE-jS2YUFOwdoWMIzyW1s0cEEdr_P0dH7_P',
    api_base_url='https://sumit-gupta.us.auth0.com',
    access_token_url='https://sumit-gupta.us.auth0.com/oauth/token',
    authorize_url='https://sumit-gupta.us.auth0.com/authorize',
    client_kwargs={'scope': 'openid profile email'}
)

def init_auth0(app):
    app.secret_key = 'cXC_JXEBFVcoAgIxrsc0t8X3snfdslE-jS2YUFOwdoWMIzyW1s0cEEdr_P0dH7_P'
    oauth = OAuth(app)
    global auth0
    auth0 = oauth.register('auth0', ...)

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated
