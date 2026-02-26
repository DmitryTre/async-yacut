from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import (
    ERROR_MISSING_REQUEST_BODY,
    ERROR_MISSING_URL_FIELD,
    ERROR_SHORT_ID_NOT_FOUND,
)
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Создаёт короткую ссылку из переданного URL через API."""
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(ERROR_MISSING_REQUEST_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(ERROR_MISSING_URL_FIELD)
    try:
        url_map = URLMap.create_from_api_data(
            original_url=data['url'],
            short=data.get('custom_id'),
            validate=True
        )
        return jsonify(
            {
                'url': data['url'],
                'short_link': url_map.get_short_url()
            }
        ), HTTPStatus.Created
    except ValueError as e:
        InvalidAPIUsage(e)


@app.route('/api/id/<short>/', methods=['GET'])
def get_original_url(short):
    """Возвращает оригинальный URL по короткой ссылке через API."""
    if not (url_map := URLMap.get_by_short(short)):
        raise InvalidAPIUsage(ERROR_SHORT_ID_NOT_FOUND, HTTPStatus.NOT_FOUND)

    return jsonify({'url': url_map.original}), HTTPStatus.OK
