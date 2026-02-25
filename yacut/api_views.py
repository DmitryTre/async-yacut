from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .constants import (
    ERROR_MISSING_REQUEST_BODY,
    ERROR_MISSING_URL_FIELD,
    ERROR_SHORT_ID_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND
)


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Создаёт короткую ссылку из переданного URL через API."""
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(ERROR_MISSING_REQUEST_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(ERROR_MISSING_URL_FIELD)

    link = URLMap.create_from_api_data(data)
    return jsonify(
        {
            'url': link.original,
            'short_link': link.get_short_url()
        }
    ), HTTP_201_CREATED


@app.route('/api/id/<short>/', methods=['GET'])
def get_original_url(short):
    """Возвращает оригинальный URL по короткой ссылке через API."""
    link = URLMap.get_by_short(short)
    if not link:
        raise InvalidAPIUsage(ERROR_SHORT_ID_NOT_FOUND, HTTP_404_NOT_FOUND)

    return jsonify({'url': link.original}), HTTP_200_OK
