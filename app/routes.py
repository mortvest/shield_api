from flask import json, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_raw_jwt

from schema import Schema, And, Use, Optional

from app import app, jwt
from app.response import *
from app.models import *


def form_response(data):
    return jsonify(data.serialize())

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedToken.is_jti_blacklisted(jti)

@app.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return form_response(ErrorResponse())
    data = request.json
    check = And(str, lambda s: len(s) > 3 and len(s) <= 64)
    schema = Schema({'username': check,
                      'password': check,
                      'first_name': check,
                      'last_name': check
                     })

    if schema.is_valid(data):
        already_exists = User.query.filter_by(username=data["username"]).first()
        if already_exists:
            return form_response(ErrorResponse("username already exists"))
        else:
            u = User(data["username"], data["password"], data["first_name"], data["last_name"])
            u.add()
            return form_response(SingleResponse({}))
    return form_response(ErrorResponse("wrong data format"))


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return form_response(ErrorResponse())

    data = request.json
    check = And(str, lambda s: len(s) > 3 and len(s) <= 64)
    schema = Schema({'username': check,
                      'password': check
                     })

    if schema.is_valid(data):
        user = User.query.filter_by(username=data["username"]).first()
        if user and user.check_password(data["password"]):
            access_token = create_access_token(identity=data["username"])
            return form_response(SingleResponse({"token": access_token}))
    return form_response(ErrorResponse("wrong username or password"))

@jwt.unauthorized_loader
def unauthorized_loader_callback(_):
    return form_response(AuthorizationErrorResponse())

@jwt.invalid_token_loader
def invalid_token_loader_callback(_):
    return form_response(AuthorizationErrorResponse())

@jwt.revoked_token_loader
def revoked_token_loader_callback():
    return form_response(AuthorizationErrorResponse())


@app.route('/logout')
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    rt = RevokedToken(jti)
    rt.add()
    return form_response(SingleResponse({}))

@app.route('/user')
@jwt_required
def users():
    users = User.query.paginate()
    return form_response(ListResponse(users))


@app.route('/user/<user_id>/')
@jwt_required
def user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return form_response(SingleResponse(user))
    else:
        return form_response(ErrorResponse())

@app.route('/user/<user_id>/posts')
@jwt_required
def user_posts(user_id):
    posts = LinkedinPost.query.filter_by(user_id=user_id).paginate()
    return form_response(ListResponse(posts))


@app.route('/posts')
@jwt_required
def posts():
    posts = LinkedinPost.query.paginate()
    return form_response(ListResponse(posts))

@app.route('/posts/<post_id>')
@jwt_required
def post(post_id):
    post = User.query.filter_by(id=post_id).first()
    if post:
        return form_response(SingleResponse(post))
    else:
        return form_response(ErrorResponse())

@app.route('/posts/<post_id>/statistics')
@jwt_required
def post_stats(post_id):
    stats = LinkedinPostStatistic.query.filter_by(linkedin_post_id=post_id).paginate()
    return form_response(ListResponse(stats))


@app.route('/statistics')
@jwt_required
def statistics_all():
    statistics = LinkedinPostStatistic.query.paginate()
    return form_response(ListResponse(statistics))

@app.route('/statistics/<statistics_id>')
@jwt_required
def statistics(statistics_id):
    stat = LinkedinPostStatistic.query.filter_by(id=statistics_id).first()
    if stat:
        return form_response(SingleResponse(stat))
    else:
        return form_response(ErrorResponse())
