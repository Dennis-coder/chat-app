from flask import request, abort, g
from functools import wraps
import models.group as Group
import jwt


class Auth:

    def login(self, roles=None):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                auth_header = request.headers.get("authorization")
                [schema, token] = auth_header.split(' ')

                if schema != "Bearer":
                    abort(401, "Wrong authorization schema")

                try:
                    user = jwt.decode(token, "secret", algorithms="HS256")
                    g.auth_user = user
                except jwt.ExpiredSignatureError:
                    abort(401, 'Signature expired. Please log in again.')
                except jwt.InvalidTokenError:
                    abort(401, 'Invalid token. Please log in again.')

                if roles and user["role"] not in roles:
                    abort(403, "Unauthorized Access")

                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def group_owner(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            group_id = request.json["group_id"] if request.json else request.args["group_id"]
            group = Group.get(group_id)
            if group["owner"] != self.user_id() and self.user_role() != 'admin':
                abort(403, "Only the group owner can access this resource")
            return func(*args, **kwargs)
        return wrapper

    def group_member(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            group_id = request.json["group_id"] if request.json else request.args["group_id"]
            is_member = Group.is_member(group_id, self.user_id())
            if not is_member and self.user_role() != 'admin':
                abort(403, "Only group members can access this resource")
            return func(*args, **kwargs)
        return wrapper

    def user(self):
        if hasattr(g, 'auth_user'):
            return g.auth_user

    def user_id(self):
        if hasattr(g, 'auth_user'):
            return g.auth_user['id']

    def user_role(self):
        if hasattr(g, 'auth_user'):
            return g.auth_user['role']
