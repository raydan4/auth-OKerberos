from flask import Flask, request, jsonify
from functools import wraps
from crypt import aes256_decrypt
from base64 import b64decode
from json import loads
from requests import post
from urllib.parse import urljoin


def gen_response(code, message):
    response = jsonify({
        'status': code,
        'message': message
    })
    response.status_code = code
    return response


def validate_token(token):
    # Decode and decrypt token
    raw = b64decode(token)
    token = aes256_decrypt(raw, app.secret_key).decode('utf-8')
    # Post token to verification endpoint
    verification_response = post(app.oauth_endpoint, data={'access_token': token})
    verification_json = verification_response.json()
    if verification_json.get('success') == True:
        return True
    else:
        return False


def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            # Get json body from request
            json = loads(request.json)
            assert json
            # Get token from body
            token =  json.get('token')
            # Assert token exists
            assert token
            # Assert token is valid
            assert validate_token(token)
            # If authorized, proceed with function call
            return f()
        except AssertionError:
            return gen_response(403, "UNAUTHORIZED")
        except ValueError, TypeError:
            return gen_response(400, "INVALID TOKEN")
    return decorator


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
@auth_required
def root():
    return gen_response(200, "AUTHORIZED")


if __name__ == "__main__":
    try:
        needed = "config file"
        import config
        needed = "KEY"
        app.secret_key = config.KEY
        needed = "OAUTH_URL and OAUTH_VALIDATION_ENDPOINT"
        app.oauth_endpoint = urljoin(config.OAUTH_URL, config.OAUTH_VALIDATION_ENDPOINT)
    except Exception:
        print(f'FATAL: missing {needed}')
        exit(1)
    app.run()