from flask import Flask, request, jsonify
from functools import wraps
from crypt import aes256_decrypt
from base64 import b64decode
from json import loads


def gen_response(code, message):
    response = jsonify({
        'status': code,
        'message': message
    })
    response.status_code = code
    return response


def validate_token(token):
    raw = b64decode(token)
    message = aes256_decrypt(raw, app.secret_key)
    json = loads(message)
    return True


def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            # Get json body from request
            json = request.json
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
        except ValueError:
            return gen_response(400, "INVALID TOKEN")
    return decorator


app = Flask(__name__)


@app.route('/', methods=['POST'])
@auth_required
def root():
    return gen_response(200, "AUTHORIZED")


if __name__ == "__main__":
    from os import urandom
    app.secret_key = urandom(16)
    print(app.secret_key)
    app.run()