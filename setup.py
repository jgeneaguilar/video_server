import os

from setuptools import setup, find_packages

requires = [
    "plaster_pastedeploy",
    "pyramid",
    "pyramid_jinja2",
    "pyramid_debugtoolbar",
    "waitress",
    "alembic",
    "pyramid_retry",
    "pyramid_tm",
    "SQLAlchemy",
    "transaction",
    "zope.sqlalchemy",
    "ipython",
    "pyramid_ipython",
    "black",
    "psycopg2",
    "psycopg2-binary",
    "bcrypt",
    "pyramid-jwt",
    "paginate",
    "paginate-sqlalchemy",
]

tests_require = [
    "WebTest >= 1.3.1",  # py3 compat
    "pytest >= 3.7.4",
    "pytest-cov",
]

setup(
    name="video_server",
    version="0.0",
    description="video_server",
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="Gene A",
    author_email="jgeneaguilar@gmail.com",
    url="",
    keywords="web pyramid pylons",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={"testing": tests_require,},
    install_requires=requires,
    entry_points={
        "paste.app_factory": ["main = video_server:main",],
        "console_scripts": ["initialize_db=video_server.scripts.initialize_db:main",],
    },
)
