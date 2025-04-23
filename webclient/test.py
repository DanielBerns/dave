from webclient import login_user, get_token_headers

USER = sys.argv[1]
PASSWORD = sys.argv[2]

def main() -> None:
    response = login_user(USER, PASSWORD)
    auth_headers
