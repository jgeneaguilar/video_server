import datetime


def format_date(date_obj):
    if isinstance(date_obj, (datetime.date, datetime.datetime)):
        return date_obj.isoformat()


def encode_user(obj):
    return {
        "id": str(obj.id),
        "username": obj.username,
        "mobile_token": obj.mobile_token,
        "created_at": format_date(obj.created_at),
        "updated_at": format_date(obj.updated_at),
    }


def encode_response_token(obj, request):
    user = encode_user(obj)
    response = {
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
        "created_at": format_date(obj.created_at),
        "updated_at": format_date(obj.updated_at),
    }


def encode_error_message(code, message):
    return {"status_code": code, "message": str(message)}
