from pyramid.view import (
    notfound_view_config,
    exception_view_config,
    forbidden_view_config,
)
from pyramid.httpexceptions import (
    HTTPServerError,
    HTTPBadRequest,
    HTTPUnauthorized,
)
from ..services.encoding import encode_error_message


@notfound_view_config(renderer="json")
def notfound_view(message, request):
    request.response.status = 404
    return encode_error_message(request.response.status_int, message)


@exception_view_config(HTTPServerError, renderer="json")
def client_error_view(message, request):
    request.response.status = 500
    return encode_error_message(request.response.status_int, message)


@exception_view_config(HTTPBadRequest, renderer="json")
def exc_bad_request_view(message, request):
    request.response.status = 400
    return encode_error_message(request.response.status_int, message)


@forbidden_view_config(renderer="json")
def forbidden_view(message, request):
    request.response.status = 403
    return encode_error_message(request.response.status_int, message)
