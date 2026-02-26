from http import HTTPStatus
from datetime import datetime, timezone
import random

from yacut import db
from flask import flash, url_for

from .constants import (
    SHORT,
    MAX_GENERATION_ATTEMPTS,
    VALID_CHARS,
    RESERVED_IDS,
    SHORT_LEN,
    LINKS_COUNT ,
    ORIGINAL_LENGTH,
    REDIRECT_ENDPOINT
)

TOO_LONG_URL = (
    'Длина URL не должна превышать'
    f' {ORIGINAL_LENGTH} символов'
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
            if (short not in RESERVED_IDS and
                    not URLMap.query.filter_by(short=short).first()):
                return short
        raise RuntimeError(ERROR_GENERATION_FAILED)

    @staticmethod
    def create(url, short, validate=True):
        """Создаёт объект URLMap из данных API-запроса."""
        if len(url) > ORIGINAL_LENGTH:
            raise ValueError(TOO_LONG_URL)

        if short:
            if short in RESERVED_IDS or URLMap.get(short):
                raise ValueError(ERROR_DOUBLE_SHORT_ID)
            if len(short) > SHORT_LEN:
                raise ValueError(INVALID_SHORT)
            if not all(char in VALID_CHARS for char in short):
                raise ValueError(INVALID_SHORT)
        else:
            short = URLMap.get_unique_short()

        url_map = URLMap(original=url, short=short)
        db.session.add(url_map)
        return url_map

    @staticmethod
    def get(short):
        """Находит запись по короткой ссылке."""
        return URLMap.query.filter_by(short=short).first()

    def get_short_url(self):
        """Рассчитывает полный URL короткой ссылки (обычный метод)."""
        return url_for(
            REDIRECT_ENDPOINT, short=self.short, _external=True
        )

    @staticmethod
    def create_batch(urls, shorts=None):
        """Создаёт пакет записей URLMap с одним коммитом в конце."""
        url_maps = []

        if shorts is None:
            shorts = [None] * len(urls)

        for url, short in zip(urls, shorts):
            url_map = URLMap.create(url, short)
            url_maps.append(url_map)

        db.session.commit()
        return url_maps