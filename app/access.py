from functools import wraps

from flask import jsonify
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt_claims
)

from app import jwt
from app.response import *
from app.models import *


class Permission():
    """
    Decorator creator class for access restriction creation
    """
    def __init__(self, groups):
        if not isinstance(groups, list):
            raise TypeError("groups must be a list")
        self.groups = groups

    def __call__(self, fn, *args, **kwargs):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            if set.intersection(set(self.groups), set(claims['groups'])) == set():
                return form_response(AuthorizationErrorResponse())
            else:
                return fn(*args, **kwargs)
        return wrapper


@jwt.unauthorized_loader
def unauthorized_loader_callback(_):
    return form_response(AuthorizationErrorResponse())


@jwt.invalid_token_loader
def invalid_token_loader_callback(_):
    return form_response(AuthorizationErrorResponse())


@jwt.revoked_token_loader
def revoked_token_loader_callback():
    return form_response(AuthorizationErrorResponse())


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedToken.is_jti_blacklisted(jti)


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    u = User.query.filter_by(username=identity).first()
    if u:
        groups = u.get_group_names()
        return {'groups': groups}
    else:
        raise ValueError("User was not found")


def form_response(data):
    return jsonify(data.serialize())
