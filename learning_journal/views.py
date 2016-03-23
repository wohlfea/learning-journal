# -*- coding: utf-8 -*-
from learning_journal.models import Entry, DBSession
from learning_journal.security import check_password
from wtforms import Form, StringField, TextAreaField, validators
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.security import remember, forget


@view_config(route_name='index',
             renderer='templates/list.jinja2')
def post_index(request):
    entries = DBSession.query(Entry).all()
    return {'entries': entries}


@view_config(route_name='entry',
             renderer='templates/entry.jinja2')
def view_post(request):
    entry_id = '{id}'.format(**request.matchdict)
    entry = DBSession.query(Entry).get(entry_id)
    return {'entry': entry}


@view_config(route_name='add',
             renderer='templates/add.jinja2',
             permission='edit')
def add_post(request):
    form = EntryForm(request.POST)
    if request.method == 'POST' and form.validate():
        entry = Entry()
        entry.title = form.title.data
        entry.text = form.text.data
        DBSession.add(entry)
        DBSession.flush()
        entry_id = entry.id
        url = request.route_url('entry', id=entry_id)
        return HTTPFound(url)
    return {'form': form}


@view_config(route_name='edit',
             renderer='templates/add.jinja2',
             permission='edit')
def edit_post(request):
    entry_id = request.matchdict['id']
    entry = DBSession.query(Entry).get(entry_id)
    form = EntryForm(request.POST, entry)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        DBSession.add(entry)
        DBSession.flush()
        url = request.route_url('entry', id=entry_id)
        return HTTPFound(url)
    return {'form': form}


@view_config(route_name='login',
             renderer='templates/login.jinja2')
def login(request):
    form = LoginForm(request.POST)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        # import pdb; pdb.set_trace()
        if check_password(password):
            headers = remember(request, username)
            return HTTPFound(location='/', headers=headers)
    return {'form': form}

@view_config(route_name='logout',
             renderer='templates/list.jinja2')
def logout(request):
    headers = forget(request)
    return HTTPFound(location='/',
                     headers=headers)


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=128)])
    password = StringField('Password', [validators.Length(min=1, max=128)])


class EntryForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=128)])
    text = TextAreaField('Content')
