from pyramid.view import forbidden_view_config, view_config
from pyramid.httpexceptions import HTTPUnauthorized, exception_response

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
    """Authenticate the user by checking the username-password combination.
        Params:
            username: string
            password: string
        Return:
            dict of id(uuid), username(string), token(jwt)
    """
    user = _authenticate_user(request)

    if user is not None:
        return encoding.encode_response_token(user, request)
    else:
        raise HTTPUnauthorized()
