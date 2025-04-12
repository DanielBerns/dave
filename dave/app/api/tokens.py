from flask import jsonify, Response
from application.api import bp
from application.api.auth import basic_auth, token_auth

@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token() -> Response:
    token = basic_auth.current_user().get_token()
    return jsonify({'token': token})


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token() -> Tuple[str, int]:
    token_auth.current_user().revoke_token()
    return '', 204
