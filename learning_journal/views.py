# -*- coding: utf-8 -*-
from learning_journal.models import Entry, DBSession
from learning_journal.security import check_password
from learning_journal.forms import LoginForm, EntryForm
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
import os


@view_config(route_name='index',
             renderer='templates/list.jinja2')
def post_index(request):
    entries = DBSession.query(Entry).all()
    return {'entries': entries}


# @view_config(route_name='index_json',
#              renderer='json',
#              xhr=True)
# def post_index(request):
#     entries = DBSession.query(Entry).all()
#     return {'entries': entries}


@view_config(route_name='entry',
             renderer='templates/entry.jinja2')
def view_post(request):
    entry_id = '{id}'.format(**request.matchdict)
    entry = DBSession.query(Entry).get(entry_id)
    return {'entry': entry}


# @view_config(route_name='entry_json',
#              renderer='json')
# def view_post(request):
#     entry_id = '{id}'.format(**request.matchdict)
#     entry = DBSession.query(Entry).get(entry_id)
#     return {'entry': entry}


@view_config(route_name='add',
             request_method='GET',
             renderer='templates/add.jinja2',
             permission='edit')
@view_config(route_name='add',
             check_csrf=True,
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


# @view_config(route_name='add_json',
#              renderer='json',
#              xhr=True)
# def add_ajax_post(request):
#     form = EntryForm(request.POST)
#     if request.method == 'POST' and form.validate():
#         entry = Entry()
#         entry.title = form.title.data
#         entry.text = form.text.data
#         DBSession.add(entry)
#         DBSession.flush()
#         entry_id = entry.id
#         entry = DBSession.query(Entry).get(entry_id)
#         return {'entry': entry}
#     return {'form': form}


@view_config(route_name='edit',
             request_method='GET',
             renderer='templates/add.jinja2',
             permission='edit')
@view_config(route_name='edit',
             check_csrf=True,
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


# @view_config(route_name='edit_json', request_method='GET',
#              renderer='json', permission='edit')
# @view_config(route_name='edit_json', check_csrf=True,
#              renderer='json', permission='edit')
# def edit_post(request):
#     entry_id = request.matchdict['id']
#     entry = DBSession.query(Entry).get(entry_id)
#     form = EntryForm(request.POST, entry)
#     if request.method == 'POST' and form.validate():
#         form.populate_obj(entry)
#         DBSession.add(entry)
#         DBSession.flush()
#         url = request.route_url('entry', id=entry_id)
#         return HTTPFound(url)
#     return {'form': form}


@view_config(route_name='login',
             check_csrf=True,
             renderer='templates/login.jinja2')
@view_config(route_name='login',
             request_method='GET',
             renderer='templates/login.jinja2')
def login(request):
    form = LoginForm(request.POST)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        if username == os.environ['AUTH_USERNAME']:
            if check_password(password):
                headers = remember(request, username)
                return HTTPFound(location='/', headers=headers)
    return {'form': form}


@view_config(route_name='logout',
             renderer='templates/list.jinja2')
def logout(request):
    headers = forget(request)
    return HTTPFound(location='/', headers=headers)


# @view_config(route_name='entry_json',
#              renderer='json')
# def view_post(request):
#     entry_id = '{id}'.format(**request.matchdict)
#     entry = DBSession.query(Entry).get(entry_id)
#     return {'entry': entry}
#
#
# @view_config(route_name='add_json',
#              renderer='templates/entry.jinja2',
#              xhr=True)
# def add_ajax_post(request):
#     form = EntryForm(request.POST)
#     if request.method == 'POST' and form.validate():
#         entry = Entry()
#         entry.title = form.title.data
#         entry.text = form.text.data
#         DBSession.add(entry)
#         DBSession.flush()
#         entry_id = entry.id
#         entry = DBSession.query(Entry).get(entry_id)
#         return {'entry': entry}
#     return {'form': form}
