import aiohttp
from http import HTTPStatus
from settings import Config


API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
HEADERS = {
    'Accept': 'application/json',
    'Authorization': f'OAuth {Config.DISK_TOKEN}'
}


class YandexDiskUploader:
    """Клиент для работы с API Яндекс Диска: загрузка и получение ссылок."""

    def __init__(self, token):
        """Инициализирует клиент с токеном для API Яндекс Диска."""
        self.token = token
        self.base_url = f'{API_HOST}{API_VERSION}/disk/resources'

    async def get_upload_link(self, filename):
        """Получает URL для загрузки файла на Яндекс Диск."""
        headers = HEADERS
        params = {'path': f'/ya_cut/{filename}', 'overwrite': 'true'}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{self.base_url}/upload',
                headers=headers,
                params=params
            ) as resp:
                if resp.status != 200:
                    raise Exception(
                        f'Ошибка API: {resp.status}, '
                        f'{await resp.text()}'
                    )
                resp_json = await resp.json()
                print('Ответ API:', resp_json)
                if 'href' not in resp_json:
                    raise KeyError(
                        f'Ключ "href" отсутствует. Полный ответ: {resp_json}'
                    )
                return resp_json['href']

    async def upload_file(self, upload_url, file_content):
        """Загружает файл на Яндекс Диск по предоставленному URL."""
        async with aiohttp.ClientSession() as session:
            async with session.put(upload_url, data=file_content) as response:
                response.raise_for_status()

    async def get_download_link(self, path):
        """Получает публичную ссылку для скачивания файла с Яндекс Диска."""
        async with aiohttp.ClientSession(headers=HEADERS) as session:
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
                    raise ValueError(
                        f'В ответе отсутствует ключ "href". '
                        f'Полный ответ: {response_json}'
                    )
                return href