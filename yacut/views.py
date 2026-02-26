from http import HTTPStatus
from flask import abort, flash, redirect, render_template
import yaml

from yacut import app
from yacut.forms import FileUploadForm, HeadURLForm
from yacut.models import URLMap
from yacut.yandex_disk import YandexDiskUploader
from .constants import REDIRECT_ENDPOINT


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
    urls_set = await uploader.upload_files(files)
    try:
        return render_template(
            'upload_files.html',
            form=form,
            uploaded_files=[
                {
                    'short': URLMap.create(
                        url=item,
                        short=None
                    ).get_short_url()
                }
                for item in urls_set
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
    with open('openapi.yml', 'r', encoding='utf-8') as f:
        openapi_data = yaml.safe_load(f)
    return render_template('help.html', openapi_content=yaml.dump(
        openapi_data,
        default_flow_style=False,
        allow_unicode=True)
    )
