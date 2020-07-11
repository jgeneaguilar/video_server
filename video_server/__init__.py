import os
from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application."""

    settings["sqlalchemy.url"] = os.getenv("DATABASE_URL")
    with Configurator(settings=settings) as config:
        config.include(".models")
        config.include(".routes")
        config.include(".security")
        config.scan()
    return config.make_wsgi_app()
