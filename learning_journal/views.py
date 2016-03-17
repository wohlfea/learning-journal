from pyramid.view import view_config


@view_config(route_name='my_route', renderer='templates/index.jinja2')
def list_view(request):
