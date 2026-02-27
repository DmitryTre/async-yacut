from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

ERROR_MISSING_REQUEST_BODY = 'Отсутствует тело запроса'
ERROR_MISSING_URL_FIELD = '"url" является обязательным полем!'
ERROR_SHORT_ID_NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Создаёт короткую ссылку из переданного URL через API."""
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(ERROR_MISSING_REQUEST_BODY)
    if 'url' not in data or None:
        raise InvalidAPIUsage(ERROR_MISSING_URL_FIELD)
    if data['url'] is None:
        raise InvalidAPIUsage(ERROR_MISSING_URL_FIELD)
    try:
        return jsonify(
            {
                'url': data['url'],
                'short_link': URLMap.create(
                    url=data['url'],
                    short=data.get('custom_id')
                ).get_short_url()
            }
        ), HTTPStatus.CREATED
    except Exception as e:
        raise InvalidAPIUsage(str(e))


@app.route('/api/id/<short>/', methods=['GET'])
def get_original_url(short):
    """Возвращает оригинальный URL по короткой ссылке через API."""
    if not (url_map := URLMap.get(short)):
        raise InvalidAPIUsage(ERROR_SHORT_ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
