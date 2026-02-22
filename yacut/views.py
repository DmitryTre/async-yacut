
import asyncio
import aiohttp
import os
import random
import string
from dotenv import load_dotenv

from flask import abort, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
from http import HTTPStatus

from . import app, db

from yacut.forms import FileUploadForm, HeadURLForm
from yacut.models import URLMap
from yacut.yandex_disk import YandexDiskUploader

load_dotenv()


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = HeadURLForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if custom_id:
            if URLMap.query.filter_by(short=custom_id).first() or custom_id == 'files':
                flash('Предложенный вариант короткой ссылки уже существует.')
                return render_template('index.html', form=form)
        else:
            custom_id = URLMap.get_unique_short_id()
        url_map = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(url_map)
        db.session.commit()
        short_link = url_for(
            'redirect_to_url',
            short_link=custom_id,
            _external=True
        )
        flash(f'Короткая ссылка создана: {url_map.short}')
        return render_template(
            'index.html',
            form=form,
            short_link=short_link,
            short_id=custom_id
        )
    return render_template('index.html', form=form)


@app.route('/files/', methods=['GET', 'POST'], strict_slashes=False)
async def upload_files():
    form = FileUploadForm()
    if request.method == 'GET':
        return render_template('upload_files.html', form=form)
    files = request.files.getlist('files')
    if not files:
        flash('Нет файлов для загрузки')
        return render_template('upload_files.html', form=form), 200

    token = os.getenv('DISK_TOKEN')
    uploader = YandexDiskUploader(token=token)
    results = []

    for file in files:
        filename = secure_filename(file.filename)
        file_data = file.read()

        upload_url = await uploader.get_upload_link(filename)

        await uploader.upload_file(upload_url, file_data)

        public_url = await uploader.get_download_link(f'/ya_cut/{filename}')
        print("Полученная ссылка на скачивание:", public_url)

        short_link = URLMap.get_unique_short_id()
        display_link = url_for(
            'redirect_to_url',
            short_link=short_link,
            _external=True
        )

        results.append({
            'filename': file.filename,
            'short_link': display_link
        })

        url_map = URLMap(
            original=public_url,
            short=short_link
        )
        print("Сохранённая ссылка в URLMap.original:", url_map.original)
        db.session.add(url_map)
        db.session.commit()

    return render_template(
        'upload_files.html',
        form=form,
        uploaded_files=results
    ), 200


@app.route('/<short_link>/', strict_slashes=False)
def redirect_to_url(short_link):
    url_map = URLMap.query.filter_by(short=short_link).first()
    if url_map:
        print(f"Нашёл запись: short={url_map.short}, original={url_map.original}")
        return redirect(url_map.original, HTTPStatus.FOUND)
    else:
        print(f"Запись не найдена для short_link={short_link}")
        return abort(404)
