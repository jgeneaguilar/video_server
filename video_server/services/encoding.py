def encode_user(object):
    _id = str(object.id)
    return {"id": _id, "username": object.username}
