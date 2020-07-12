from pyramid.view import view_config
from pyramid.httpexceptions import HTTPForbidden, HTTPNotFound, HTTPBadRequest

from ..models import Room, RoomMembership, User
from ..services import encoding


# Room public views
@view_config(
    route_name="room", request_method="GET", renderer="json",
)
def get_room_info(request):
    """Retrieve information about a room.
        Return:
            dict of id(uuid), name(string), host_id(uuid), capacity(int), members(list)
    """
    room_id = request.matchdict["room_id"]
    room = request.dbsession.query(Room).filter(Room.id == room_id).first()

    if room is not None:
        members = [encoding.encode_user(user) for user in room.users]
        room_info = encoding.encode_room(room, members=members)

        return room_info
    else:
        raise HTTPNotFound()


# Room auth views
@view_config(
    route_name="rooms", request_method="POST", renderer="json", permission="auth",
)
def create_room(request):
    """Create a room for an authenticated user and set user as the host.
        Params:
            name: string
            capacity: int (optional)
        Return:
            dict of id(uuid), name(string), host_id(uuid), capacity(int)
    """
    user_id = request.authenticated_userid
    name = request.json_body.get("name")
    capacity = request.json_body.get("capacity")  # 5 as default

    if capacity is not None:
        if capacity < 2:
            raise HTTPBadRequest("Room capacity must be at least 2.")
        if capacity >= 50:
            raise HTTPBadRequest("Maximum room capacity is 50.")

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
    route_name="host", request_method="PATCH", renderer="json", permission="auth",
)
def change_host(request):
    """Change the room host. Current user must be a host.
        Params:
            new_host_id: string (uuid)
        Return:
            dict of id(uuid), name(string), host_id(uuid), capacity(int)
    """
    user_id = request.authenticated_userid
    room_id = request.matchdict["room_id"]
    request.json = request.json_body or {}
    new_host_id = request.json.get("new_host_id")
    if new_host_id is None:
        raise HTTPNotFound("Please enter a valid new host id.")

    session = request.dbsession
    room = session.query(Room).filter_by(id=room_id).first()
    # check if new_host is a member of the room
    new_host_membership_id = (
        session.query(RoomMembership.user_id)
        .filter(
            RoomMembership.user_id == new_host_id, RoomMembership.room_id == room_id
        )
        .scalar()
    )

    if room is None:
        raise HTTPNotFound("The room cannot be found.")
    if new_host_membership_id is None:
        raise HTTPNotFound("Please enter a valid user as host.")

    if new_host_membership_id is not None and room is not None:
        if user_id == new_host_membership_id:
            raise HTTPForbidden("Current user is already the host.")
        if user_id == str(room.host_id):
            room.host_id = new_host_membership_id
            return encoding.encode_room(room)
        else:
            raise HTTPForbidden("Current user is not the host.")


@view_config(
    route_name="room_members",
    request_method="POST",
    renderer="json",
    permission="auth",
)
def join_room(request):
    """Enable the user to join a room if still within room capacity and if user is not already a member."""
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
    elif user_id in members:
        raise HTTPForbidden("You have already joined the room.")
    elif not len(members) < room_capacity:
        raise HTTPForbidden("The room is already full.")


@view_config(
    route_name="room_members",
    request_method="DELETE",
    renderer="json",
    permission="auth",
)
def leave_room(request):
    """Delete the user membership record."""
    user_id = request.authenticated_userid
    room_id = request.matchdict["room_id"]

    session = request.dbsession
    room_membership = (
        session.query(RoomMembership)
        .filter(RoomMembership.room_id == room_id, RoomMembership.user_id == user_id)
        .first()
    )

    if room_membership is not None:
        session.delete(room_membership)
        return "Success"
    else:
        raise HTTPNotFound("You have not joined this room.")
