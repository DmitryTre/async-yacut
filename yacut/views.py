from http import HTTPStatus
from flask import abort, redirect, render_template

from yacut import app
from yacut.forms import FileUploadForm, HeadURLForm
from yacut.models import URLMap
from yacut.yandex_disk import YandexDiskUploader
from .constants import (
    DISK_TOKEN,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND
)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Отображает форму создания короткой ссылки и обрабатывает её отправку."""
    form = HeadURLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short = URLMap.create(
        form.original_link.data,
        form.custom_id.data
    ).get_short_url()
    return render_template(
        'index.html',
        form=form,
        short=short
    )


@app.route('/files/', methods=['GET', 'POST'], strict_slashes=False)
async def upload_files():
    """Отображает форму загрузки файлов и обрабатывает загрузку на Я.Диск."""
    form = FileUploadForm()
    if not form.validate_on_submit():
        return render_template('upload_files.html', form=form)
    files = form.files.data
    uploader = YandexDiskUploader(token=DISK_TOKEN)
    results = await uploader.upload_files(files)
    return render_template(
        'upload_files.html',
        form=form,
        uploaded_files=[
            {
                'filename': item['filename'],
                'short': URLMap.create(
                    original_link=item['download_link']
                ).get_short_url()
            }
            for item in results
        ]
    ), HTTP_200_OK


@app.route('/<short>/', endpoint='redirect_to_url', strict_slashes=False)
def redirect_to_url(short=None):
    """Перенаправляет по короткой ссылке на оригинальный URL."""
    original = URLMap.get_original_url(short)
    if original:
        return redirect(original, HTTPStatus.FOUND)
    return abort(HTTP_404_NOT_FOUND)


@app.route('/help')
def help_page():
    """Маршрут для отображения страницы справки."""
    return render_template('help.html')