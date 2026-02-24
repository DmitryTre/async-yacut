import aiohttp
from http import HTTPStatus

from .error_handlers import InvalidAPIUsage
from .constants import (
    API_HOST,
    API_VERSION,
    DOWNLOAD_LINK_URL,
    ERROR_DOWNLOAD_LINK,
    REQUEST_UPLOAD_URL,
    HEADERS,
    HREF_KEY_ERROR,
    YA_CUT_PATH_PREFIX
)


class YandexDiskUploader:
    """Клиент для работы с API Яндекс Диска: загрузка и получение ссылок."""

    def __init__(self, token):
        """Инициализирует клиент с токеном для API Яндекс Диска."""
        self.token = token
        self.base_url = f'{API_HOST}{API_VERSION}/disk/resources'
        self.headers = HEADERS.copy()

    async def get_upload_link(self, filename):
        """Получает URL для загрузки файла на Яндекс Диск."""
        params = {'path': f'{filename}', 'overwrite': 'true'}
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(
                REQUEST_UPLOAD_URL,
                params=params
            ) as resp:
                if resp.status != HTTPStatus.OK:
                    raise InvalidAPIUsage(
                        message=ERROR_DOWNLOAD_LINK,
                        status_code=resp.status
                    )
                resp_json = await resp.json()
                if 'href' not in resp_json:
                    raise KeyError(HREF_KEY_ERROR)
                return resp_json['href']

    async def upload_file(self, upload_url, file_content):
        """Загружает файл на Яндекс Диск по предоставленному URL."""
        async with aiohttp.ClientSession() as session:
            async with session.put(upload_url, data=file_content) as response:
                response.raise_for_status()

    async def get_download_link(self, path):
        """Получает публичную ссылку для скачивания файла с Яндекс Диска."""
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(
                url=DOWNLOAD_LINK_URL,
                params={'path': path}
            ) as response:
                response.raise_for_status()

                if response.status == HTTPStatus.NO_CONTENT:
                    raise ValueError('API вернул статус 204 No Content')

                response_json = await response.json()
                href = response_json.get('href')
                if not href:
                    raise ValueError(HREF_KEY_ERROR)
                return href

    async def upload_file_to_ya_disk(self, file):
        """Загружает файл на Яндекс Диск и возвращает публичную ссылку."""
        path = f'{YA_CUT_PATH_PREFIX}{file.filename}'
        file_data = file.read()
        await self.upload_file(await self.get_upload_link(path), file_data)
        return await self.get_download_link(path)

    async def upload_files(self, files):
        """Асинхронная загрузка файлов."""
        return [
            {
                'filename': file.filename,
                'download_link': await self.upload_file_to_ya_disk(file)
            }
            for file in files
        ]
