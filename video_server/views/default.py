from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models

# User public views
@view_config(
    route_name="users", request_method="GET", renderer="json",
)
def get_all_users(request):
    """Retrieves all registered users"""
    pass


@view_config(
    route_name="user", request_method="GET", renderer="json",
)
def get_user_by_username(request):
    """Retrieves a user by its username"""
    pass


@view_config(
    route_name="create_user", request_method="POST", renderer="json",
)
def create_user(request):
    """Creates a new user and authenticates session"""
    pass


# User auth views
@view_config(
    route_name="change_password",
    request_method="PUT",
    renderer="json",
    permission="auth",
)
def change_password(request):
    """Changes an authenticated user's password"""
    pass


@view_config(
    route_name="change_mobile_token",
    request_method="PUT",
    renderer="json",
    permission="auth",
)
def change_mobile_token(request):
    """Changes an authenticated user's mobile token"""
    pass


@view_config(
    route_name="delete_user",
    request_method="DELETE",
    renderer="json",
    permission="auth",
)
def delete_user(request):
    """Deletes an authenticated user's account"""
    pass


# Room public views
@view_config(
    route_name="get_room_info", request_method="GET", renderer="json",
)
def get_room_info(request):
    """
    Retrieves information about a room:
        - room name
        - host name
        - list of members
    """
    pass


@view_config(
    route_name="get_user_rooms", request_method="GET", renderer="json",
)
def get_rooms_by_username(request):
    """Retrieves a list of rooms a user is in"""
    pass


# Room auth views
@view_config(
    route_name="create_room", request_method="POST", renderer="json", permission="auth",
)
def create_room(request):
    """Creates a room for an authenticated user and set user as the host"""
    pass


@view_config(
    route_name="change_host", request_method="PUT", renderer="json", permission="auth",
)
def change_host(request):
    """Changes the room host. Current user must be a host"""
    pass


@view_config(
    route_name="join_room", request_method="POST", renderer="json", permission="auth",
)
def join_room(request):
    """Enables the user to join a room if still within room capacity"""
    pass


@view_config(
    route_name="leave_room",
    request_method="DELETE",
    renderer="json",
    permission="auth",
)
def leave_room(request):
    """Removes the user from the room"""
    pass


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
