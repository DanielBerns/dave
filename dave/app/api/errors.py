from flask import jsonify, Response
from werkzeug.http import HTTP_STATUS_CODES


def error_response(
    status_code: int,
    message: str | None = None
) -> Response:
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    payload['message'] = message if message else "no content"
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(
    message: str
) -> Response:
    return error_response(400, message)
