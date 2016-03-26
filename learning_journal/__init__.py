from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import SignedCookieSessionFactory
from .models import (
    DBSession,
    Base,
    MyRoot,
    )
import os


def make_session(settings):
    from sqlalchemy.orm import sessionmaker
    engine = engine_from_config(settings, 'sqlalchemy.')
    Session = sessionmaker(bind=engine)
    return Session()


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    if 'DATABASE_URL' in os.environ:
        settings['sqlalchemy.url'] = os.environ['DATABASE_URL']
    engine = engine_from_config(settings, 'sqlalchemy.')
    auth_secret = os.environ.get('AUTH_SECRET', 'secret')
    authn_policy = AuthTktAuthenticationPolicy(secret=auth_secret,
                                               hashalg='sha256')
    authz_policy = ACLAuthorizationPolicy()
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(
        settings=settings,
        root_factory=MyRoot)
    config.set_session_factory(SignedCookieSessionFactory('seekrit'))
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('add', '/add')
    config.add_route('entry', '/entries/{id:\d+}')
    config.add_route('edit', '/entries/{id:\d+}/edit')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    # config.add_route('add_json', '/add_json')
    # config.add_route('entry_json', '/entry_json')
    config.scan()
    return config.make_wsgi_app()
