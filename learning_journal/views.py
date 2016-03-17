from pyramid.view import view_config
from .models import (Entry, DBSession)
from wtforms import Form, StringField, validators


@view_config(route_name='index_route', renderer='templates/list.jinja2')
def index_view(request):
    entries = DBSession.query(Entry).all()
    return {'entries': entries}


@view_config(route_name='entry_route', renderer='templates/entry.jinja2')
def entry_view(request):
    # to see what's in the request, put a pdb
    # set_trace() here and look at the request object
    # look at the object itself and see what's
    # in the documentation for that object type (dir())
    # entry_id = '{entry}'.format(**request.matchdict)
    entry_id = request.matchdict['entry']
    entry_data = DBSession.query(Entry).get(entry_id)
    # entry_data = DBSession.query(Entry).filter(Entry.id == entry_id).first()
    return {'entry': entry_data}


class RegistrationForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=128), validators.])


# use predicate to specify a specific view only for a POST request
