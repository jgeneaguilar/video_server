def includeme(config):
    # User public routes
    config.add_route("users", "/users")
    config.add_route("create_user", "/users/create")
    config.add_route("user", "/users/find/{username}")
    config.add_route("login", "/login")

    # User auth routes
    config.add_route("change_password", "/users/me/password")
    config.add_route("change_mobile_token", "/users/me/mobile_token")
    config.add_route("delete_user", "/users/me/delete")

    # Room public routes
    config.add_route("get_room_info", "/rooms/info/{room_id}")
    config.add_route("get_user_rooms", "/rooms/list/{username}")

    # Room auth routes
    config.add_route("create_room", "/rooms/create")
    config.add_route("change_host", "/rooms/{room_id}/host")
    config.add_route("join_room", "/rooms/{room_id}/members/join")
    config.add_route("leave_room", "/rooms/{room_id}/members/leave")
