
from datetime import datetime, timezone
import random

from flask import url_for

from yacut import db
from yacut.constants import (
    MAX_GENERATION_ATTEMPTS,
    ORIGINAL_LENGTH,
    REDIRECT_ENDPOINT,
    RESERVED_SHORT,
    SHORT,
    SHORT_LEN,
    VALID_CHARS,
    VALID_SHORT_REGEX
)

TOO_LONG_URL = (
    'Длина URL не должна превышать'
    f'{ORIGINAL_LENGTH} символов'
)
ERROR_DOUBLE_SHORT_ID = 'Предложенный вариант короткой ссылки уже существует.'
ERROR_GENERATION_FAILED = 'Сбой генерации после {MAX_GENERATION_ATTEMPTS} раз'
INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'


class URLMap(db.Model):
    """Модель хранения соответствий URL и коротких ссылок."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LENGTH))
    short = db.Column(db.String(SHORT), unique=True, index=True)
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=lambda: datetime.now(timezone.utc)
    )

    @staticmethod
    def get_unique_short():
        """Генерирует уникальный короткий ID для ссылки."""
        for _ in range(MAX_GENERATION_ATTEMPTS):
            short = ''.join(random.choices(VALID_CHARS, k=SHORT))
            if (short not in RESERVED_SHORT and
                    not URLMap.get(short)):
                return short
        raise RuntimeError(ERROR_GENERATION_FAILED)

    @staticmethod
    def create(url, short=None, validate=True, commit=True):
        """Создаёт объект URLMap из данных API-запроса."""
        if validate:
            if len(url) > ORIGINAL_LENGTH:
                raise ValueError(TOO_LONG_URL)
            if short:
                if (len(short) > SHORT_LEN
                        or not VALID_SHORT_REGEX.match(short)):
                    raise ValueError(INVALID_SHORT)
                if short in RESERVED_SHORT or URLMap.get(short):
                    raise ValueError(ERROR_DOUBLE_SHORT_ID)
            else:
                short = URLMap.get_unique_short()
        url_map = URLMap(original=url, short=short)
        db.session.add(url_map)
        if commit:
            db.session.commit()
        return url_map

    @staticmethod
    def get(short):
        """Находит запись по короткой ссылке."""
        return URLMap.query.filter_by(short=short).first()

    def get_short_url(self):
        """Рассчитывает полный URL короткой ссылки."""
        return url_for(
            REDIRECT_ENDPOINT, short=self.short, _external=True
        )
