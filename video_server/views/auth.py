from pyramid.view import forbidden_view_config, view_config
from pyramid.httpexceptions import HTTPUnauthorized

from ..models import User
from ..services import encoding


def _authenticate_user(request):
    username = request.json_body.get("username")
    password = request.json_body.get("password")
    user = request.dbsession.query(User).filter_by(username=username).first()

    if user is not None and user.check_password(password):
        return user
    else:
        return None


@view_config(
    route_name="login", request_method="POST", renderer="json",
)
def login(request):
    """Authenticates the user by checking the username-password combination"""
    user = _authenticate_user(request)

    if user is not None:
        return encoding.encode_response_token(user, request)
    else:
        raise HTTPUnauthorized()


@forbidden_view_config()
def forbidden_view(request):
    return "Unauthorized"
