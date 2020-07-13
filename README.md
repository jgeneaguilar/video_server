# video_server
A simple REST API built using Pyramid, SQLAlchemy and PostgreSQL. It is a user and room management api for video conferencing.
The app is hosted on Heroku at https://pyramid-video-server.herokuapp.com/


## Features
- A user can create an "account" and manage it by updating the password and/or mobile token and deleting the account.
- An authenticated user can create a room, be its host and set a capacity limit for the room.
- As a host, a user can change a room's host.
- An authenticated user can join or leave a room.


## Authentication
The server uses JWT (JSON Web Tokens) for authentication by sending requests with a bearer token in the authorization header. It makes use of the pyramid-jwt library. Authenticated views are protected using Pyramid's built-in Authorization Policy.


## Pagination
For routes that return *all* resources, pagination is implemented. The default is to limit responses to 1 page containing 10 items. These limitations can be customized through the query parameters.


## Limitations (For now)
- Validation


## Database Schema
The data is stored in a PostgreSQL database.

- User = { id, username, password_hash, mobile_token, created_at, updated_at, rooms (relationship to Room) }
- Room = { id, name, host_id (foreign key), host(relationship to User), capacity, created_at, updated_at, users (relationship to Users }
- RoomMembership = { id, user_id (foreign key), room_id (foreign key), created_at, updated_at }