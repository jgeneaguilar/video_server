from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Authenticated, Everyone

from .models import User


class AuthenticationPolicy(AuthTktAuthenticationPolicy):
    def authenticated_userid(self, request):
        """Returns the authenticated userid or None"""
        user = request.user
        if user is not None:
            return user.id

        def effective_principals(self, request):
            """Returns a list of effective principals derived from request"""
            principals = [Everyone]
            user = request.user
            if user is not None:
                principals.append(Authenticated)
                principals.append(str(user.id))
            return principals


def get_user(request):
    """Convers the unauthenticated_userid from the policy into a User object from the db"""
    user_id = request.unauthenticated_userid
    if user_id is not None:
        user = request.dbsession.query(User).get(user_id)
        return user


def includeme(config):
    settings = config.get_settings()
    authn_policy = AuthenticationPolicy(settings["auth.secret"], hashalg="sha512",)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(ACLAuthorizationPolicy)
    config.add_request_method(get_user, "user", reify=True)
