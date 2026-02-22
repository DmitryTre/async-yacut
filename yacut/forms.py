from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length


class HeadURLForm(FlaskForm):
    """Форма для ввода URL и пользовательского ID короткой ссылки."""

    original_link = URLField(
        'Оригинальная ссылка',
        validators=(
            DataRequired(message='Поле обязательно для заполнения'),
            Length(
                max=2048,
                message='Ссылка слишком длинная (максимум 2048 символов)'
            ),
        ),
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=(
            Length(
                max=16,
                message='Ссылка слишком длинная (максимум 16 символов)'
            ),
        )
    )
    submit = SubmitField('Создать')


class FileUploadForm(FlaskForm):
    """Форма для загрузки одного или нескольких файлов на сервер."""

    files = MultipleFileField(
        'Выберите файлы для загрузки',
        validators=(DataRequired(message='Надо выбрать хотя бы один файл'),),
    )
    submit = SubmitField('Загрузить файлы')
