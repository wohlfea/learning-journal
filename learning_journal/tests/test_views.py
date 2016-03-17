# -​*- coding: utf-8 -*​-

from learning_journal.views import entry_view


@pytest.fixture(scope='function')
def dummytransaction():
    new_model = Entry(title='test entry', text='this entry is just a test.')
    DBSession.add(new_model)
    DBSession.flush()


def test_entry_view_id(dbtransaction):
    test_request.matchdict = {'id': new_model.id}
    dic = entry_view(test_request)
    assert dic['single_entry'].title == 'jill'


def test_entry_view_text(dbtransaction):
    test_request.matchdict = {'id': new_model.id}
    dic = entry_view(test_request)
    assert dic['single_entry'].text == 'jello'


def test_home_view(dbtransaction):
    dic = home_view(test_request)
    assert dic['entry_list'].all()[0].title == 'jill'


def test_home_view_sort(dbtransaction):
    dic = home_view(test_request)
    assert dic['entry_list'].all()[1].title == 'jill'


def test_entry_view(dbtransaction):
    test_request.matchdict = {'id': new_model.id}
    dic = entry_view(test_request)
    assert dic['single_entry'] == new_model
