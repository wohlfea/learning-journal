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
    entry_id = '{id}'.format(**request.matchdict)
    entry_data = DBSession.query(Entry).filter(Entry.id == entry_id).first()
    return {'entry': entry_data}


@view_config(route_name='new_route', renderer='templates/add.jinja2')
def add_view(request):
    form = EntryForm(request.POST)
    if request.method == 'POST' and form.validate():
        entry = Entry()
        entry.title = form.title.data
        entry.text = form.text.data
        # import pdb; pdb.set_trace()
        DBSession.add(entry)
        DBSession.flush()
        entry_id = entry.id
        url = request.route_url('entry_route', id=entry_id)
        return HTTPFound(url)
    return {'form': form, 'action': request.matchdict.get('action')}


# @view_config(route_name='edit_route', renderer='templates/edit.jinja2')
# def edit_view(request):
#     entry_id = request.matchdict['entry']


class EntryForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=128)])
    text = TextAreaField('Content')


# def get_form_entry(request):
#     form = EntryForm(request.POST)
#     if request.method == 'POST' and form.validate():
#         entry = Entry()
#         entry.title = form.title.data
#         entry.text = form.text.data
#         # import pdb; pdb.set_trace()
#         DBSession.add(entry)
#         DBSession.flush()
#         entry_id = entry.id
#         url = request.route_url('entry_route', detail_id=entry_id)
#         return HTTPFound(url)
#     return form
