from pyramid.view import view_config
from .models import Entry, DBSession
from wtforms import Form, StringField, TextAreaField, validators
from pyramid.httpexceptions import HTTPFound


@view_config(route_name='index_route', renderer='templates/list.jinja2')
def index_view(request):
    entries = DBSession.query(Entry).all()
    return {'entries': entries}


@view_config(route_name='entry_route', renderer='templates/entry.jinja2')
def entry_view(request):
    entry_id = '{entry}'.format(**request.matchdict)
    entry_data = DBSession.query(Entry).filter(Entry.id == entry_id).first()
    return {'entry': entry_data}


@view_config(route_name='new_route', renderer='templates/add.jinja2')
def add_view(request):
    form = get_form_entry(request)
    return {'form': form}


# @view_config(route_name='edit_route', renderer='templates/edit.jinja2')
# def edit_view(request):
#     entry_id = request.matchdict['entry']


class EntryForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=128)])
    text = TextAreaField('Content', [validators.InputRequired()])


def get_form_entry(request):
    form = EntryForm(request.POST)
    if request.method == 'POST' and form.validate():
        entry = Entry()
        entry.title = form.title
        entry.text = form.text
        DBSession.add(entry)
        return HTTPFound(location="/entry/{id}")
    return {'form': form, 'action': request.matchdict.get('action')}
