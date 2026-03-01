from http import HTTPStatus
import os

from flask import abort, flash, redirect, render_template, send_file

from yacut import app
from yacut.constants import REDIRECT_ENDPOINT
from yacut.forms import FileUploadForm, HeadURLForm
from yacut.models import URLMap
from yacut.yandex_disk import upload_files as upload_files_to_disk


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Отображает форму создания короткой ссылки и обрабатывает её отправку."""
    form = HeadURLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short=URLMap.create(
                url=form.original_link.data,
                short=form.custom_id.data,
                skip_form_validations=True
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
    if not files:
        flash('Не выбрано ни одного файла для загрузки', 'error')
        return render_template('upload_files.html', form=form)
    try:
        urls = await upload_files_to_disk(files)
    except (RuntimeError, ValueError) as e:
        flash(str(e), 'error')
        return render_template('upload_files.html', form=form)
    try:
        return render_template(
            'upload_files.html',
            form=form,
            uploaded_files=[
                {
                    'name': file.filename,
                    'short': URLMap.create(
                        url=direct_url,
                        commit=(file == files[-1])
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