import os
from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application."""

    # Get
    settings["sqlalchemy.url"] = os.environ["DATABASE_URL"]
    with Configurator(settings=settings) as config:
        config.include(".models")
        config.include("pyramid_jinja2")
        config.include(".routes")
        config.include(".security")
        config.scan()
    return config.make_wsgi_app()
