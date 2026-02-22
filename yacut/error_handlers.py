from flask import jsonify, render_template, request

from . import app, db


class InvalidAPIUsage(Exception):
    """Исключение для ошибок API с настраиваемым статусом и сообщением."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """Инициализирует исключение."""
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Возвращает словарь с сообщением об ошибке для JSON-ответа."""
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error: InvalidAPIUsage):
    """Обрабатывает пользовательские исключения API."""
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(400)
def bad_request(error):
    """Обрабатывает ошибки 400 Bad Request."""
    if request.content_type == 'application/json':
        return jsonify({'message': 'Отсутствует тело запроса'}), 400
    return error


@app.errorhandler(404)
def page_not_found(error):
    """Обрабатывает ошибки 404 Not Found, отображает шаблон 404.html."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Обрабатывает ошибки 500 Internal Server Error"""
    db.session.rollback()
    return render_template('500.html'), 500
