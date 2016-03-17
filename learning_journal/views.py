from pyramid.view import view_config
from .models import (Entry, DBSession)


@view_config(route_name='index_route', renderer='templates/base.jinja2')
def index_view(request):
    entries = DBSession.query(Entry).all()
    print('************', entries)
    return {'entries': entries}


@view_config(route_name='entry_route', renderer='templates/entry.jinja2')
def entry_view(request):
    entry_id = '{entry}'.format(**request.matchdict)
    entry_data = DBSession.query(Entry).filter(Entry.id == entry_id).first()
    return {'entry': entry_data}
