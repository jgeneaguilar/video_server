import os
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Authenticated, Everyone, Allow


class Root(object):
    """Defines the permissions of the views"""

    def __init__(self, request):
        self.request = request

    # only Authenticated users can access "permission='auth'" views
    __acl__ = [(Allow, Authenticated, "auth")]


def includeme(config):
    """Security-related configuration"""
    auth_secret = os.environ["AUTH_SECRET"]
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.include("pyramid_jwt")
    config.set_jwt_authentication_policy(
        auth_secret, auth_type="Bearer", expiration=43200
    )
    config.set_root_factory(Root)
