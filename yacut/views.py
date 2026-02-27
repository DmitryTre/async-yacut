from http import HTTPStatus
import os

from flask import abort, flash, redirect, render_template, send_file

from yacut import app
from yacut.constants import REDIRECT_ENDPOINT
from yacut.forms import FileUploadForm, HeadURLForm
from yacut.models import URLMap
from yacut.yandex_disk import YandexDiskUploader


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Отображает форму создания короткой ссылки и обрабатывает её отправку."""
    form = HeadURLForm()
    if form.validate_on_submit():
        try:
            return render_template(
                'index.html',
                form=form,
                short=URLMap.create(
                    form.original_link.data,
                    form.custom_id.data
                ).get_short_url()
            )
        except (RuntimeError, ValueError) as e:
            flash(str(e), 'error')
    return render_template('index.html', form=form)


@app.route('/files/', methods=['GET', 'POST'], strict_slashes=False)
async def upload_files():
    """Отображает форму загрузки файлов и обрабатывает загрузку на Я.Диск."""
    form = FileUploadForm()
    if not form.validate_on_submit():
        return render_template('upload_files.html', form=form)
    files = form.files.data
    uploader = YandexDiskUploader()
    try:
        urls = await uploader.upload_files(files)
        return render_template(
            'upload_files.html',
            form=form,
            uploaded_files=[
                {
                    'name': file.filename,
                    'short': URLMap.create(
                        url=direct_url
                    ).get_short_url()
                }
                for file, direct_url in zip(files, urls)
            ]
        )
    except (RuntimeError, ValueError) as e:
        flash(str(e), 'error')
        return render_template('upload_files.html', form=form)


@app.route('/<short>', endpoint=REDIRECT_ENDPOINT, strict_slashes=False)
def redirect_to_url(short):
    """Перенаправляет по короткой ссылке на оригинальный URL."""
    if (url_map := URLMap.get(short)):
        return redirect(url_map.original, HTTPStatus.FOUND)
    return abort(HTTPStatus.NOT_FOUND)


@app.route('/help')
def help_page():
    """Маршрут для отображения страницы справки."""
    return send_file(
        os.path.join(os.path.dirname(__file__), 'openapi.yml'),
        mimetype='text/yaml',
        as_attachment=False
    )