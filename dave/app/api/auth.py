from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, Response
from application.models import User
from application.dbops import DBOps
from application.api.errors import error_response


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(
    username: str,
    password: str
) -> User | None:
    user = DBOps.get_user_by_username(username)
    return user if user and user.check_password(password) else None


@basic_auth.error_handler
def basic_auth_error(
    status: int
) -> Response:
    return error_response(status)


@token_auth.verify_token
def verify_token(
    token: str
) -> User | None:
    return DBOps.check_token(token)


@token_auth.error_handler
def token_auth_error(
    status: int
) -> Response:
    return error_response(status)
