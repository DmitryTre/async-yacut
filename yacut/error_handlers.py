from http import HTTPStatus
from flask import jsonify, render_template, request

from . import app, db
from .constants import ERROR_MISSING_REQUEST_BODY


class InvalidAPIUsage(Exception):
    """Исключение для ошибок API с настраиваемым статусом и сообщением."""

    def __init__(self, message, status_code=HTTPStatus.BAD_REQUEST):
        """Инициализирует исключение."""
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        """Возвращает словарь с сообщением об ошибке для JSON-ответа."""
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error: InvalidAPIUsage):
    """Обрабатывает пользовательские исключения API."""
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.BAD_REQUEST)
def bad_request(error):
    """Обрабатывает ошибки 400 Bad Request."""
    if request.content_type == 'application/json':
        return jsonify(
            {'message': ERROR_MISSING_REQUEST_BODY}
        ), HTTPStatus.BAD_REQUEST
    return error


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    """Обрабатывает ошибки 404 Not Found, отображает шаблон 404.html."""
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    """Обрабатывает ошибки 500 Internal Server Error."""
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
