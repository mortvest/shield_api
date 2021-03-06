import datetime as dt
import traceback
from functools import wraps


from flask import json, jsonify, request
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_raw_jwt,
)
from schema import Schema, And, Use, Optional

from app import app, jwt
from app.response import *
from app.models import *
from app.access import *


class route(object):
    @classmethod
    def form_response(cls, data):
        return jsonify(data.serialize())

    def __init__(self, path, methods=None):
        self.path = path
        self.methods = methods

    def __call__(self, fn):
        @app.route(self.path, methods=self.methods)
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                result = fn(*args, **kwargs)
                return route.form_response(result)
            except:
                traceback.print_exc()
                return route.form_response(ErrorResponse(""))
        return wrapper


def json_receiver(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.is_json:
            return fn(*args, **kwargs)
        else:
            return ErrorResponse("expecting a json")
    return wrapper


@route('/register', methods=['POST'])
@json_receiver
def register():
    data = request.json
    check = User.string_check(64)
    schema = Schema({'username': check,
                     'password': check,
                     'first_name': check,
                     'last_name': check
                    })
    if schema.is_valid(data):
        # check if username is already in the database
        already_exists = User.query.filter_by(username=data["username"]).first()
        if already_exists:
            return ErrorResponse("username already exists")
        else:
            user = User(data["username"], data["password"], data["first_name"], data["last_name"])
            group = UserGroup.query.filter_by(group_name="user").first()
            user.groups.append(group)
            user.add()
            return SingleResponse()
    return ErrorResponse("wrong data format")


@route('/login', methods=['POST'])
@json_receiver
def login():
    data = request.json
    check = And(str, lambda s: len(s) > 0 and len(s) <= 64)
    schema = Schema({'username': check,
                     'password': check
                     })

    if schema.is_valid(data):
        user = User.query.filter_by(username=data["username"]).first()
        if user and user.check_password(data["password"]):
            access_token = create_access_token(identity=data["username"])
            return SingleResponse({"token": access_token})
    return ErrorResponse("wrong username or password")


@route('/logout', methods=['POST'])
@user_permission
def logout():
    # get the token data
    jti = get_raw_jwt()['jti']
    # revoke the token by adding it to the database
    rt = RevokedToken(jti)
    rt.add()
    return SingleResponse()


@route('/user')
@admin_permission
def users():
    users = User.query.paginate()
    return ListResponse(users)


@route('/user/<user_id>/', methods=['GET'])
@admin_permission
def user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return SingleResponse(user)
    else:
        return ErrorResponse()


@route('/user/<user_id>/posts', methods=['GET'])
@user_permission
def user_posts(user_id):
    posts = LinkedinPost.query.filter_by(user_id=user_id).paginate()
    return ListResponse(posts)


@route('/posts', methods=['GET'])
@user_permission
def posts():
    posts = LinkedinPost.query.paginate()
    return ListResponse(posts)


@route('/posts', methods=['POST'])
@user_permission
@json_receiver
def add_post():
    data = request.json
    schema = Schema({Optional("id"): int,
                     "user_id": LinkedinPost.id_check,
                     "content": LinkedinPost.string_check(512)
                    })
    if schema.is_valid(data):
        # check if user_id exists
        if User.query.filter_by(id=data['user_id']).first():
            post = LinkedinPost(data['user_id'], content=data['content'])
            post.add()
            return SingleResponse()
    return ErrorResponse("wrong data format")


@route('/posts/<post_id>', methods=['GET'])
@user_permission
def get_post(post_id):
    post = User.query.filter_by(id=post_id).first()
    if post:
        return SingleResponse(post)
    else:
        return ErrorResponse()


@route('/posts/<post_id>', methods=['PUT'])
@admin_permission
@json_receiver
def update_post(post_id):
    data = request.json
    schema = Schema({Optional("id"): int,
                     Optional("user_id"): int,
                     "content": LinkedinPost.string_check(512)
                    })
    if schema.is_valid(data):
        post = LinkedinPost.query.filter_by(id=int(post_id)).first()
        if post:
            post.content = data['content']
            post.update()
            return SingleResponse()
        return ErrorResponse("post could not be found")
    return ErrorResponse("wrong data format")


@route('/posts/<post_id>', methods=['DELETE'])
@admin_permission
def delete_post(post_id):
    post = LinkedinPost.query.filter_by(id=int(post_id)).first()
    if post:
        post.delete()
        return SingleResponse()
    return ErrorResponse("post could not be found")


@route('/posts/<post_id>/statistics', methods=['GET'])
@user_permission
def post_stats(post_id):
    stats = LinkedinPostStatistic.query.filter_by(linkedin_post_id=post_id).paginate()
    return ListResponse(stats)


@route('/statistics', methods=['GET'])
@user_permission
def statistics_all():
    statistics = LinkedinPostStatistic.query.paginate()
    return ListResponse(statistics)


@route('/statistics/', methods=['POST'])
@user_permission
@json_receiver
def post_statistics():
    data = request.json
    check = LinkedinPost.id_check
    schema = Schema({Optional("id"): int,
                     "linkedin_post_id": check,
                     "num_views": check,
                     "num_likes": check,
                     "num_comments": check
                    })
    if schema.is_valid(data):
        # check if linkedin_post_id exists
        if LinkedinPost.query.filter_by(id=data['linkedin_post_id']).first():
            stat = LinkedinPostStatistic(linkedin_post_id=data['linkedin_post_id'],
                                         num_views=data['num_views'],
                                         num_likes=data['num_likes'],
                                         num_comments=data['num_comments'])
            stat.add()
            return SingleResponse()
        return ErrorResponse("post does not exist")
    return ErrorResponse("wrong data format")



@route('/statistics/<statistics_id>', methods=['GET'])
@user_permission
def statistics(statistics_id):
    stat = LinkedinPostStatistic.query.filter_by(id=statistics_id).first()
    if stat:
        return SingleResponse(stat)
    else:
        return ErrorResponse()


@route('/statistics/<statistics_id>', methods=['PUT'])
@admin_permission
@json_receiver
def update_statistics(statistics_id):
    if not request.is_json:
        return ErrorResponse()
    data = request.json
    check = LinkedinPost.id_check
    schema = Schema({Optional("id"): int,
                     "linkedin_post_id": check,
                     "num_views": check,
                     "num_likes": check,
                     "num_comments": check
                    })
    if schema.is_valid(data):
        # check if statistic exists
        stat = LinkedinPost.query.filter_by(id=int(statistics_id)).first()
        if stat:
            stat.linkedin_post_id = data['linkedin_post_id']
            stat.num_views = data['num_views']
            stat.num_likes = data['num_likes']
            stat.num_comments = data['num_comments']
            stat.update()
            return SingleResponse()
        return ErrorResponse("statistic does not exist")
    return ErrorResponse("wrong data format")


@route('/statistics/<statistics_id>', methods=['DELETE'])
@admin_permission
def delete_statistics(statistics_id):
    stat = LinkedinPostStatistic.query.filter_by(id=int(statistics_id)).first()
    if stat:
        stat.delete()
        return SingleResponse()
    return ErrorResponse("statistics could not be found")
