from pyramid.view import view_config
from .models import (Entry, DBSession)
from wtforms import Form, StringField, TextAreaField, validators


@view_config(route_name='index_route', renderer='templates/list.jinja2')
def index_view(request):
    entries = DBSession.query(Entry).all()
    return {'entries': entries}


@view_config(route_name='entry_route', renderer='templates/entry.jinja2')
def entry_view(request):
    entry_id = request.matchdict['entry']
    entry_data = DBSession.query(Entry).get(entry_id)
    return {'entry': entry_data}


@view_config(route_name='add_route', renderer='templates/add.jinja2')
def add_view(request):
    raw_add = get_form_entry(request)
    return {'template': raw_add}


@view_config(route_name='edit_route', renderer='templates/edit.jinja2')
def edit_view(request):
    entry_id = request.matchdict['entry']


class EntryForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=128)])
    text = TextAreaField('Content')


def get_form_entry(request):
    form = EntryForm(request.POST)
    if request.method == 'POST' and form.validate():
        title = form.title
        text = form.text
        return HTTPFound(location="/entry/{id}")


# use predicate to specify a specific view only for a POST request
