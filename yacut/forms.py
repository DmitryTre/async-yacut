from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Regexp, Length, Optional

from .constants import (
    LABEL_CUSTOM_ID,
    LABEL_ORIGINAL_LINK,
    LABEL_SUBMIT_SHORTEN,
    LABEL_FILES,
    LABEL_SUBMIT_UPLOAD,
    MSG_FIELD_REQUIRED,
    MSG_INVALID_SHORT_ID_CHARS,
    MSG_URL_TOO_LONG,
    MSG_SHORT_ID_TOO_LONG,
    MSG_NO_FILES_SELECTED,
    ORIGINAL_LENGHT,
    VALID_CHARS,
    SHORT_LEN,
)


class HeadURLForm(FlaskForm):
    """Форма для ввода URL и пользовательского ID короткой ссылки."""

    original_link = URLField(
        LABEL_ORIGINAL_LINK,
        validators=(
            DataRequired(message=MSG_FIELD_REQUIRED),
            Length(
                max=ORIGINAL_LENGHT,
                message=MSG_URL_TOO_LONG.format(max_length=ORIGINAL_LENGHT)
            ),
        ),
    )
    custom_id = StringField(
        LABEL_CUSTOM_ID,
        validators=(
            Regexp(
                regex=f'^[{VALID_CHARS}]*$',
                message=MSG_INVALID_SHORT_ID_CHARS
            ),
            Length(
                max=SHORT_LEN,
                message=MSG_SHORT_ID_TOO_LONG.format(max_length=SHORT_LEN)
            ),
            Optional()
        )
    )
    submit = SubmitField(LABEL_SUBMIT_SHORTEN)


class FileUploadForm(FlaskForm):
    """Форма для загрузки одного или нескольких файлов на сервер."""

    files = MultipleFileField(
        LABEL_FILES,
        validators=(DataRequired(message=MSG_NO_FILES_SELECTED),),
    )
    submit = SubmitField(LABEL_SUBMIT_UPLOAD)
