import aiohttp

from http import HTTPStatus

from .constants import (
    DOWNLOAD_LINK_URL,
    HEADERS,
    NO_CONTENT,
    REQUEST_UPLOAD_URL,
)
from settings import Config


async def get_upload_link(filename):
    """Получает URL для загрузки файла на Яндекс Диск."""
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(
            REQUEST_UPLOAD_URL,
            params={'path': filename, 'overwrite': 'true'}
        ) as resp:
            resp.raise_for_status()
            return (await resp.json())['href']


async def upload_file(upload_url, file_content):
    """Загружает файл на Яндекс Диск по предоставленному URL."""
    async with aiohttp.ClientSession() as session:
        async with session.put(upload_url, data=file_content) as response:
            response.raise_for_status()


async def get_download_link(path):
    """Получает публичную ссылку для скачивания файла с Яндекс Диска."""
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(
            url=DOWNLOAD_LINK_URL,
            params={'path': path}
        ) as response:
            response.raise_for_status()
            if response.status == HTTPStatus.NO_CONTENT:
                raise ValueError(NO_CONTENT)
            return (await response.json()).get('href')


async def upload_file_to_ya_disk(file):
    """Загружает файл на Яндекс Диск и возвращает публичную ссылку."""
    path = f'{Config.YA_CUT_BASE_PATH}{file.filename}'
    await upload_file(await get_upload_link(path), file.read())
    return await get_download_link(path)


async def upload_files(files):
    """Асинхронная загрузка файлов."""
    return [await upload_file_to_ya_disk(file) for file in files]