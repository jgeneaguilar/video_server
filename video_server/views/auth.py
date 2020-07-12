from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound

from ..models import User
from ..services import encoding


def _authenticate_user(request):
    username = request.json_body.get("username")
    password = request.json_body.get("password")
    user = request.dbsession.query(User).filter_by(username=username).first()

    if user is not None:
        if user.check_password(password):
            return user
        else:
            raise HTTPBadRequest("The password you have entered is incorrect.")
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
        return {"data": encoding.encode_response_token(user, request)}
    else:
        raise HTTPNotFound()
