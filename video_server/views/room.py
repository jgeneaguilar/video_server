from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import exception_response

from ..models import Room, RoomMembership, User
from ..services import encoding


# Room public views
@view_config(
    route_name="get_room_info", request_method="GET", renderer="json",
)
def get_room_info(request):
    """
    Retrieves information about a room:
        - room name
        - host name
        - capacity
        - list of members
    """
    room_id = request.matchdict["room_id"]
    room = request.dbsession.query(Room).filter(Room.id == room_id).first()

    if room is not None:
        members = [encoding.encode_user(user) for user in room.users]
        room_info = encoding.encode_room(room, members=members)

        return room_info
    else:
        raise exception_response(404)


# members = [
#        str(i[0])
#        for i in session.query(User.id)
#        .join(RoomMembership)
#        .filter(RoomMembership.room_id == room_id)
#        .all()
#    ]


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
    user_id = request.authenticated_userid
    name = request.json_body.get("name")
    capacity = request.json_body.get("capacity")  # 5 as default

    session = request.dbsession
    new_room = Room(name=name, capacity=capacity, host_id=user_id)
    session.add(new_room)
    session.flush()

    # add host as member
    new_member = RoomMembership(user_id=user_id, room_id=new_room.id)
    session.add(new_member)
    session.flush()

    return encoding.encode_room(new_room)


@view_config(
    route_name="change_host",
    request_method="PATCH",
    renderer="json",
    permission="auth",
)
def change_host(request):
    """
        Changes the room host. Current user must be a host

        params:
            new_host_id: string (uuid)

        auth user from request
        room id from request url
    """
    user_id = request.authenticated_userid
    room_id = request.matchdict["room_id"]
    new_host_id = request.json_body.get("new_host_id")

    session = request.dbsession
    room = session.query(Room).filter_by(id=room_id).first()

    if user_id == str(room.host_id):
        room.host_id = new_host_id
        return encoding.encode_room(room)
    else:
        raise exception_response(403)


@view_config(
    route_name="join_room", request_method="POST", renderer="json", permission="auth",
)
def join_room(request):
    """Enables the user to join a room if still within room capacity and user is not already a member"""
    user_id = request.authenticated_userid
    room_id = request.matchdict["room_id"]

    session = request.dbsession
    members = [
        str(i[0])
        for i in session.query(User.id)
        .join(RoomMembership)
        .filter(RoomMembership.room_id == room_id)
        .all()
    ]
    room_capacity = session.query(Room.capacity).filter_by(id=room_id).scalar()

    if user_id not in members and len(members) < room_capacity:
        new_member = RoomMembership(user_id=user_id, room_id=room_id)
        session.add(new_member)
        session.flush()

        return {
            "id": str(new_member.id),
            "user_id": str(new_member.user_id),
            "room_id": str(new_member.room_id),
        }
    else:
        raise exception_response(403)


@view_config(
    route_name="leave_room",
    request_method="DELETE",
    renderer="json",
    permission="auth",
)
def leave_room(request):
    """Removes the user from the room"""
    user_id = request.authenticated_userid
    room_id = request.matchdict["room_id"]

    session = request.dbsession
    room_membership = session.query(RoomMembership).filter_by(room_id=room_id).first()

    if room_membership is not None and user_id == str(room_membership.user_id):
        session.delete(room_membership)
        return "Success"
    else:
        raise exception_response(403)
