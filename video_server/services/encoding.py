def encode_user(obj):
    _id = str(obj.id)
    return {"id": _id, "username": obj.username}


def encode_response_token(obj, request):
    user = encode_user(obj)
    response = {
        "request": "ok",
        **user,
        "token": request.create_jwt_token(user["id"], username=user["username"]),
    }
    return response


def encode_room(obj, **kwargs):
    _id = str(obj.id)
    host_id = str(obj.host_id)
    return {
        "id": _id,
        "name": obj.name,
        "capacity": obj.capacity,
        "host_id": host_id,
        **kwargs,
    }
