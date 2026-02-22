
import string

from flask import jsonify, request

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if data is None or not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    elif 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    custom_id = data.get('custom_id', '').strip()
    if custom_id:
        if len(custom_id) > 16 or not all(
            c in string.ascii_lowercase + string.digits for c in custom_id
        ):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        elif URLMap.query.filter_by(short=custom_id).first():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
    else:
        custom_id = URLMap.get_unique_short_id()
    link = URLMap()
    link.from_dict(data, custom_id)
    db.session.add(link)
    db.session.commit()

    return jsonify(link.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'], strict_slashes=False)
def get_original_url(short_id):
    link = URLMap.query.filter_by(short=short_id.rstrip('/')).first()
    if link is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': link.original}), 200