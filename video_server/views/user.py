from pyramid.view import view_config

from ..models import User
from ..services import encoding


# User public views
@view_config(
    route_name="users", request_method="GET", renderer="json",
)
def get_all_users(request):
    """Retrieves all registered users"""
    users = request.dbsession.query(User.id, User.username).all()
    user_list = [encoding.encode_user(user) for user in users]
    return user_list


@view_config(
    route_name="user", request_method="GET", renderer="json",
)
def get_user_by_username(request):
    """Retrieves a user by its username"""
    username = request.matchdict["username"]
    user = request.dbsession.query(User).filter_by(username=username).first()
    return encoding.encode_user(user)


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
