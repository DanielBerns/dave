from flask import jsonify, request, url_for, abort, current_app, Response
from application import db
from application.models import User, Post, Message, Store, save_image
from application.api import bp
from application.api.auth import token_auth
from application.api.errors import bad_request

from datetime import datetime

@bp.route('/users/current', methods=['GET'])
@token_auth.login_required
def get_current_user() -> Response:
    current_user = token_auth.current_user()
    return jsonify(current_user.to_dict())


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def users(id: int) -> Response:
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'password' not in data:
        return bad_request(NO_USER_CREDENTIALS)
    if User.query.filter_by(username=data['username']).first():
        return bad_request("Use a different username")
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id: int) -> Response:
    if token_auth.current_user().id != id:
        abort(403)
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and User.query.filter_by(username=data['username']).first():
        return bad_request("username update not allowed")
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())


