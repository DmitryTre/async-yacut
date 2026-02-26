
from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (
    ORIGINAL_LENGTH,
    REGEX,
    SHORT_LEN,
)

# Сообщения для валидации форм
FIELD_REQUIRED = 'Поле обязательно для заполнения'
URL_TOO_LONG = 'Ссылка длиннее {ORIGINAL_LENGTH} символов'
SHORT_ID_TOO_LONG = 'ID длиннее {SHORT_LEN} символов'
NO_FILES_SELECTED = 'Выберите хотя бы один файл'
INVALID_SHORT_ID_CHARS = 'Недопустимые символы в ID'

# Подписи полей форм
LABEL_ORIGINAL_LINK = 'Оригинальная ссылка'
LABEL_CUSTOM_ID = 'Ваш вариант короткой ссылки'
LABEL_FILES = 'Выберите файлы для загрузки'

# Надписи кнопок
LABEL_SUBMIT_SHORTEN = 'Создать'
LABEL_SUBMIT_UPLOAD = 'Загрузить файлы'


class HeadURLForm(FlaskForm):
    """Форма для ввода URL и пользовательского ID короткой ссылки."""

    original_link = URLField(
        LABEL_ORIGINAL_LINK,
        validators=(
            DataRequired(message=FIELD_REQUIRED),
            Length(
                max=ORIGINAL_LENGTH,
                message=URL_TOO_LONG
            ),
        ),
    )
    custom_id = StringField(
        LABEL_CUSTOM_ID,
        validators=(
            Regexp(
                regex=REGEX,
                message=INVALID_SHORT_ID_CHARS
            ),
            Length(
                max=SHORT_LEN,
                message=SHORT_ID_TOO_LONG
            ),
            Optional()
        )
    )
    submit = SubmitField(LABEL_SUBMIT_SHORTEN)


class FileUploadForm(FlaskForm):
    """Форма для загрузки одного или нескольких файлов на сервер."""

    files = MultipleFileField(
        LABEL_FILES,
        validators=(DataRequired(message=NO_FILES_SELECTED),),
    )
    submit = SubmitField(LABEL_SUBMIT_UPLOAD)
