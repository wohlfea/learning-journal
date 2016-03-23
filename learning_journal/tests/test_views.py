# -*- coding: utf-8 -*-
from learning_journal.views import post_index, view_post
from pyramid.testing import DummyRequest
import os

DATA_SUCCESS = {'username': 'admin', 'password': 'secret'}
DATA_FAIL_USER = {'username': 'whatever', 'password': 'secret'}


def test_post_index(dbtransaction, new_entry):
    test_request = DummyRequest()
    response_dict = post_index(test_request)
    response = response_dict['entries']
    assert response[0] == new_entry


def test_view_post(dbtransaction, new_entry):
    test_request = DummyRequest()
    test_request.matchdict = {'id': new_entry.id}
    response_dict = view_post(test_request)
    assert response_dict['entry'] == new_entry


# def test_list_response(dbtransaction, app, new_entry):
#     response = app.get('/')
#     assert response.status_code == 200
#
#
# def test_add_response(dbtransaction, app):
#     response = app.get('/add')
#     assert response.status_code == 200
#
#
# def test_detail_response(dbtransaction, app, new_entry):
#     new_entry_id = new_entry.id
#     response = app.get('/entries/{}'.format(new_entry_id))
#     assert response.status_code == 200
#
#
# def test_edit_response(dbtransaction, app, new_entry):
#     new_entry_id = new_entry.id
#     response = app.get('/entries/{}/edit'.format(new_entry_id))
#     assert response.status_code == 200


def test_password_exist(app):
    assert os.environ.get('AUTH_PASSWORD', None) is not None


def test_username_exist(app):
    assert os.environ.get('AUTH_USERNAME', None) is not None


def test_check_password_success(auth_env):
    from learning_journal.security import check_password
    password = 'secret'
    assert check_password(password)


def test_stored_password_is_encrypted(auth_env):
    assert os.environ.get('AUTH_PASSWORD', None) != 'secret'


def check_password_fails(auth_env):
    from learning_journal.security import check_password
    password = 'not secret'
    assert not check_password(password)


def test_get_login_view(app):
    response = app.get('/login')
    assert response.status_code == 200


def test_post_login_success(app, auth_env):
    response = app.post('/login', DATA_SUCCESS)
    assert response.status_code == 302


def test_post_login_password_fail(app):
    data = {'username': 'admin', 'password': 'whatever'}
    response = app.post('/login', data)
    assert response.status_code == 200


def test_post_login_username_fail(app):
    data = {'username': 'whatever', 'password': 'secret'}
    response = app.post('/login', data)
    assert response.status_code == 200
