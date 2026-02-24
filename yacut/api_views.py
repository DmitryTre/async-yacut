from flask import jsonify, request

from . import app
from .models import URLMap
from .constants import HTTP_200_OK, HTTP_201_CREATED


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Создаёт короткую ссылку из переданного URL через API."""
    data = request.get_json()
    link = URLMap.create_from_api_data(data).save()
    return jsonify(link.to_dict()), HTTP_201_CREATED


@app.route('/api/id/<short_id>/', methods=['GET'], strict_slashes=False)
def get_original_url(short):
    """Возвращает оригинальный URL по короткой ссылке через API."""
    link = URLMap.get_byshort(short)
    return jsonify({'url': link.original}), HTTP_200_OK
