from flask import render_template, request
from lynx.errors import bp


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404 # Page Not Found


@bp.app_errorhandler(405)
def method_not_found(error):
    return render_template('errors/405.html'), 405

@bp.app_errorhandler(500)
def internal_error(error):
        #db.session.rollback()
    return render_template('errors/500.html'), 500 # Server Error

@bp.app_errorhandler(401)
def not_auth_error(error):
    return render_template('errors/401.html'), 401 # UNAUTHORIZED

#custom error page
@bp.route('/error')
def error():
    #email error to developer
    return render_template('errors/error.html')