from pyramid.view import (
    notfound_view_config,
    exception_view_config,
    forbidden_view_config,
)
from pyramid.response import Response


@notfound_view_config(renderer="json")
def notfound_view(request):
    response = Response("Not found.")
    response.status_int = 404
    return response


@exception_view_config(renderer="json")
def client_error_view(request):
    response = Response(".")
    response.status_int = 500
    return response


@forbidden_view_config(renderer="json")
def forbidden_view(request):
    response = Response("Not allowed.")
    response.status_int = 403
    return response
