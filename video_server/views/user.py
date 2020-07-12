from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound

from ..models import User
from ..services import encoding


# User public views
@view_config(
    route_name="users", request_method="GET", renderer="json",
)
def get_users(request):
    """Retrieve a list all registered users or one user if username is in url query string."""
    username_query = request.GET.get("username")
    session = request.dbsession

    if username_query is not None:
        user = session.query(User).filter_by(username=username_query).first()
        if user is not None:
            return encoding.encode_user(user)
        else:
            raise HTTPNotFound()
    else:
        users = request.dbsession.query(User.id, User.username).all()
        user_list = [encoding.encode_user(user) for user in users]
        return user_list


@view_config(
    route_name="users", request_method="POST", renderer="json",
)
def create_user(request):
    """Create a new user and authenticate session.
        Params:
            username: string
            password: string
            mobile_token: string (optional)
        Return:
            dict of id(uuid), username(string), token(jwt)
    """
    username = request.json_body.get("username")
    password = request.json_body.get("password")
    mobile_token = request.json_body.get("mobile_token", "")

    session = request.dbsession
    username_exist = session.query(User).filter_by(username=username).first()

    if username_exist is not None:
        raise HTTPBadRequest("The username already exists.")

    new_user = User(username=username, password=password, mobile_token=mobile_token)
    session.add(new_user)
    session.flush()
    return encoding.encode_response_token(new_user, request)


# User auth views
@view_config(
    route_name="user_me", request_method="PATCH", renderer="json", permission="auth",
)
def update_user(request):
    """Change an authenticated user's password and/or mobile_token.
        Params:
            password: string
            mobile_token: string (optional)
    """
    user_id = request.authenticated_userid
    password = request.json_body.get("password")
    mobile_token = request.json_body.get("mobile_token")

    user = request.dbsession.query(User).filter_by(id=user_id).first()

    if user is None:
        raise HTTPNotFound()
    if password is not None:
        if not user.check_password(password):
            # check if password param is not the same
            user.set_password(password)
        else:
            raise HTTPBadRequest("You cannot use the same password.")
    if mobile_token is not None:
        user.mobile_token = mobile_token
    return "Success"


@view_config(
    route_name="user_me", request_method="DELETE", renderer="json", permission="auth",
)
def delete_user(request):
    """Delete an authenticated user's account."""
    user_id = request.authenticated_userid

    session = request.dbsession
    user = session.query(User).filter_by(id=user_id).first()
    if user is not None:
        session.delete(user)
        return "Success"
    else:
        raise HTTPNotFound()


@view_config(
    route_name="user_rooms", request_method="GET", renderer="json",
)
def get_rooms_by_username(request):
    """Retrieve a list of rooms a user is in.
        Return:
            list of dict{ id(uuid), name(string) }
    """
    username = request.matchdict["username"]

    user = request.dbsession.query(User).filter_by(username=username).first()

    if user is not None:
        rooms = [
            encoding.encode_room(
                room,
                is_host=room.host_id == user.id,
                members=[encoding.encode_user(user) for user in room.users],
            )
            for room in user.rooms
        ]
        return rooms
    else:
        raise HTTPNotFound()
