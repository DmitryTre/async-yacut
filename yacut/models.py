from datetime import datetime, timezone
import random

from yacut import db
from flask import flash, url_for

from .constants import (
    CUSTOM_SHORT,
    MAX_GENERATION_ATTEMPTS,
    VALID_CHARS,
    RESERVED_IDS,
    SHORT_LEN,
    ORIGINAL_LENGHT,
    ERROR_INVALID_SHORT_ID,
    ERROR_GENERATION_FAILED,
    ERROR_MISSING_REQUEST_BODY,
    ERROR_MISSING_URL_FIELD,
    ERROR_DOUBLE_SHORT_ID
)
from .error_handlers import InvalidAPIUsage


class URLMap(db.Model):
    """Модель хранения соответствий URL и коротких ссылок."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LENGHT))
    short = db.Column(db.String(CUSTOM_SHORT), unique=True, index=True)
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=lambda: datetime.now(timezone.utc)
    )

    @staticmethod
    def is_reserved(short: str) -> bool:
        """Проверить, является ли ID зарезервированным."""
        if short in RESERVED_IDS:
            raise InvalidAPIUsage(ERROR_DOUBLE_SHORT_ID.format(short=short))
        return False

    @staticmethod
    def is_unique(short: str) -> bool:
        """Проверить уникальность короткого ID в БД."""
        return not URLMap.query.filter_by(short=short).first()

    @staticmethod
    def validate_short(short):
        """Валидирует формат короткого ID."""
        if len(short) > SHORT_LEN:
            raise InvalidAPIUsage(ERROR_INVALID_SHORT_ID)
        if not all(c in VALID_CHARS for c in short):
            raise InvalidAPIUsage(ERROR_INVALID_SHORT_ID)

    @staticmethod
    def get_unique_short():
        """Генерирует уникальный короткий ID для ссылки."""
        for _ in range(MAX_GENERATION_ATTEMPTS):
            short = ''.join(random.choices(VALID_CHARS, k=CUSTOM_SHORT))
            if URLMap.is_reserved(short):
                continue
            if URLMap.is_unique(short):
                return short
        raise InvalidAPIUsage(
            ERROR_GENERATION_FAILED.format(attempts=MAX_GENERATION_ATTEMPTS)
        )

    @staticmethod
    def create_from_api_data(data):
        """Создаёт объект URLMap из данных API-запроса."""
        if data is None or not data:
            raise InvalidAPIUsage(ERROR_MISSING_REQUEST_BODY)

        if 'url' not in data:
            raise InvalidAPIUsage(ERROR_MISSING_URL_FIELD)

        custom_id = data.get('custom_id', '').strip()

        if custom_id:
            URLMap.validate_short(custom_id)
            URLMap.is_reserved(custom_id)
            if not URLMap.is_unique(custom_id):
                raise InvalidAPIUsage(
                    ERROR_DOUBLE_SHORT_ID.format(short=custom_id)
                )
        else:
            custom_id = URLMap.get_unique_short()

        link = URLMap()
        link.original = data['url']
        link.short = custom_id

        db.session.add(link)
        db.session.commit()
        return link

    @staticmethod
    def create(original_link, custom_id):
        """Создаёт и сохраняет в БД запись URLMap."""
        if custom_id:
            URLMap.is_reserved(custom_id)
            flash('Предложенный вариант короткой ссылки уже существует.')
            URLMap.validate_short(custom_id)

            if not URLMap.is_unique(custom_id):
                raise InvalidAPIUsage(
                    ERROR_DOUBLE_SHORT_ID.format(short=custom_id)
                )
        else:
            custom_id = URLMap.get_unique_short()

        link = URLMap(original=original_link, short=custom_id)
        db.session.add(link)
        db.session.commit()
        return link

    @classmethod
    def get_by_short(cls, short):
        """Находит запись по короткой ссылке."""
        cleaned_short = short.rstrip('/')
        return cls.query.filter_by(short=cleaned_short).first()

    def get_short_url(self):
        """Рассчитывает полный URL короткой ссылки (обычный метод)."""
        return url_for(
            'redirect_to_url', short=self.short, _external=True
        )

    @classmethod
    def get_original_url(cls, short):
        """Получает оригинальный URL по короткой ссылке."""
        url_map = cls.get_by_short(short)
        if url_map:
            return url_map.original
        return None

    @classmethod
    async def create_with_file_link(cls, original_url):
        """Создаёт запись URLMap и возвращает данные для отображения."""
        short_link = cls.get_unique_short_id()
        display_link = url_for(
            'redirect_to_url',
            short_link=short_link,
            _external=True
        )

        url_map = cls(original=original_url, short=short_link)
        db.session.add(url_map)
        db.session.commit()

        return {
            'short_link': display_link,
            'original_url': original_url
        }