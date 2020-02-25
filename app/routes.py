from flask import json, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from app import app, jwt
from app.response import *
from app.models import *


def form_response(data):
    return jsonify(data.serialize())

blacklist = set()
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

@app.route('/register')
def register():
    return "Register Page"

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return form_response(ErrorResponse())

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return form_response(ErrorResponse())

    if username != 'test' or password != 'test':
        return form_response(AuthorizationErrorResponse())

    access_token = create_access_token(identity=username)
    return form_response(SingleResponse({"token": access_token}))

@jwt.unauthorized_loader
def unauthorized_loader_callback(_):
    return form_response(AuthorizationErrorResponse())

@jwt.invalid_token_loader
def invalid_token_loader_callback(_):
    return form_response(AuthorizationErrorResponse())


@app.route('/logout')
@jwt_required
def logout():
    current_user = get_jwt_identity()
    return form_response(SingleResponse({}))


@app.route('/user')
def users():
    users = User.query.paginate()
    return form_response(ListResponse(users))


@app.route('/user/<user_id>/')
def user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return form_response(SingleResponse(user))
    else:
        return form_response(ErrorResponse())

@app.route('/user/<user_id>/posts')
def user_posts(user_id):
    posts = LinkedinPost.query.filter_by(user_id=user_id).all()
    return form_response(ListResponse(posts))


@app.route('/posts')
def posts():
    posts = LinkedinPost.query.paginate()
    return form_response(ListResponse(posts))

@app.route('/posts/<post_id>')
def post(post_id):
    post = User.query.filter_by(id=post_id).first()
    if post:
        return form_response(SingleResponse(post))
    else:
        return form_response(ErrorResponse())

@app.route('/posts/<post_id>/statistics')
def post_stats(post_id):
    stats = LinkedinPostStatistic.query.filter_by(linkedin_post_id=post_id).all()
    return form_response(ListResponse(stats))


@app.route('/statistics')
def statistics_all():
    statistics = LinkedinPostStatistic.query.all()
    return form_response(ListResponse(statistics))

@app.route('/statistics/<statistics_id>')
def statistics(statistics_id):
    stat = LinkedinPostStatistic.query.filter_by(id=statistics_id).first()
    if stat:
        return form_response(SingleResponse(stat))
    else:
        return form_response(ErrorResponse())
