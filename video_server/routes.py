def includeme(config):
    # User routes
    config.add_route("users", "/users")
    config.add_route("user_me", "/users/me")
    config.add_route("user_rooms", "/users/{username}/rooms")
    config.add_route("login", "/login")

    # Room routes
    config.add_route("rooms", "/rooms")
    config.add_route("room", "/rooms/{room_id}")
    config.add_route("host", "/rooms/{room_id}/host")
    config.add_route("room_members", "/rooms/{room_id}/members")
