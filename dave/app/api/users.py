from flask import jsonify, request, url_for, abort, current_app, Response
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.extensions import db
from app.models import User, Post, Message, Store, save_image

from datetime import datetime

@bp.route('/user/current', methods=['GET'])
@token_auth.login_required
def get_current_user() -> Response:
    current_user = token_auth.current_user()
    return jsonify(current_user.to_dict())


@bp.route('/user/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user_by_id(id: int) -> Response:
    user = DBOps.get_user_by_id(id)
    return jsonify(user.to_dict())

@bp.route('/user/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id: int) -> Response:
    if token_auth.current_user().id != id:
        abort(403)
    user = DBOps.get_user_by_id(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and User.query.filter_by(username=data['username']).first():
        return bad_request("username update not allowed")
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/user', methods=['POST'])
def create_user() -> Response:
    data = request.get_json() or {}
    username = data.get("username", None)
    email = data.get("email", None)
    password = data.get("password", None)
    repeat_password = data.get("repeat_password", None)
    user_credentials = [username, email, password, repeat_password]
    if any(not (x and len(x)) for x in user_credentials):
        return bad_request("No valid user credentials")
    user = DBOps.create_user(
        username,
        email,
        password,
        repeat_password
    )
    if user is None:
        return bad_request("No valid request")
    else:
        response = jsonify(user.to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('api.get_user', id=user.id)
        return response




