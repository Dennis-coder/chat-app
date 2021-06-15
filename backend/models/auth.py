from flask import request, abort, g
from functools import wraps
import jwt


class Auth:

    def login(self, roles=None):
        def login_decorator(func):
            @wraps(func)
            def login_wrapper(*args, **kwargs):
                auth_header = request.headers.get("authorization")
                [schema, token] = auth_header.split(' ')

                if schema != "Bearer":
                    abort(401, description="Wrong authorization schema")
                try:
                    user = jwt.decode(token, "secret", algorithms="HS256")
                except jwt.ExpiredSignatureError:
                    abort(401, description='Signature expired. Please log in again.')
                except jwt.InvalidTokenError:
                    abort(401, description='Invalid token. Please log in again.')

                if roles and user["role"] not in roles:
                    abort(403, description="Unauthorized Access")

                g.auth_user = user
                return func(*args, **kwargs)
            return login_wrapper
        return login_decorator

    def get_user(self):
        if hasattr(g, 'auth_user'):
            return g.auth_user
