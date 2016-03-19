# -*- coding: utf-8 -*-
from learning_journal.views import post_index, view_post
from pyramid.testing import DummyRequest
from learning_journal.models import DBSession, Entry


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


def test_add_post(dbtransaction, app):
    results = DBSession.query(Entry).filter(
        Entry.title == 'TEST' and Entry.text == 'TEST')
    assert results.count() == 0
    params = {
        'title': 'TEST',
        'text': 'TEST'
    }
    app.post('/add', params=params, status='3*')
    results = DBSession.query(Entry).filter(
        Entry.title == 'TEST' and Entry.text == 'TEST')
    assert results.count() == 1
