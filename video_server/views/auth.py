from pyramid.view import forbidden_view_config, view_config

from ..models import User


def _authenticate_user(request):
    username = request.json_body["username"]
    password = request.json_body["password"]
    user = request.dbsession.query(User).filter_by(username=username).first()

    if user is not None and user.check_password(password):
        user_dict = dict(id=str(user.id), username=user.username)
        return user_dict
    else:
        return None


@view_config(
    route_name="login", request_method="POST", renderer="json",
)
def login(request):
    """Authenticates the user by checking the username-password combination"""
    user = _authenticate_user(request)

    if user is not None:
        return {
            "result": "ok",
            "username": user["username"],
            "token": request.create_jwt_token(user["id"], username=user["username"]),
        }
    else:
        return "Unauthorized"


@forbidden_view_config()
def forbidden_view(request):
    return "Unauthorized"
