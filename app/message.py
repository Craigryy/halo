from app import app
from flask import jsonify, url_for


def bad_request(message):
    '''Request that are bad '''

    # response to invalid/bad  request.
    response = jsonify({'message': message, 'status': '400'})
    response.status_code = 400
    return response


def Unauthorized(message=None):
    ''' Restricted in perfroming these action .'''

    # if a message/response if secret key is given.
    if message is None:
        if app.config['SECRET_KEY']:
            message = 'Authentication with your token is needed.'
        else:
            message = 'Token is required.'
    response = jsonify({'message': message, 'status': 401})
    response.status_code = 401
    if app.config['SECRET_KEY']:
        response.headers['Location'] = url_for('new_user')
    return response


def Method_not_allowed():
    '''Method not allowed'''

    # message to response to method not allowed
    response = jsonify({'status': 405, 'error': 'method not allowed'})
    response.status_code = 405
    return response
