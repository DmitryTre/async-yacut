import os
import string

from settings import Config

# === КОНСТАНТЫ ПРИЛОЖЕНИЯ ===
SHORT_LEN = 16
SHORT = 6
ORIGINAL_LENGTH = 2048
MAX_GENERATION_ATTEMPTS = 100
VALID_CHARS = string.ascii_lowercase + string.digits
RESERVED_IDS = {'files'}
REGEX = f'^[{VALID_CHARS}]*$'

DISK_TOKEN = os.getenv('DISK_TOKEN')
REDIRECT_VIEW_NAME = 'redirect_to_url'

# === КОНСТАНТЫ СООБЩЕНИЙ ОБ ОШИБКАХ (уровень модуля) ===
ERROR_MISSING_REQUEST_BODY = 'Отсутствует тело запроса'
ERROR_INVALID_URL = 'Недопустимый URL: {url}'

ERROR_VALIDATION_FAILED = 'Ошибка валидации: {details}'
ERROR_RESERVED_SHORT_ID = 'ID "{short}" зарезервирован'
ERROR_MISSING_URL_FIELD = '"url" является обязательным полем!'
ERROR_SHORT_ID_NOT_FOUND = 'Указанный id не найден'
ERROR_DOWNLOAD_LINK = 'Ошибка получения ссылки для загрузки'

API_HOST = 'https://cloud-api.yandex.net/'
REQUEST_UPLOAD_URL = f'{API_HOST}{Config.API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{Config.API_VERSION}/disk/resources/download'
HEADERS = {
    'Accept': 'application/json',
    'Authorization': f'OAuth {Config.DISK_TOKEN}'
}
BASE_URL = f'{API_HOST}{Config.API_VERSION}/disk/resources/'
HREF_KEY_ERROR = 'Ключ href отсутствует.'
REDIRECT_ENDPOINT = 'redirect_to_url'
NO_CONTENT = 'API вернул статус 204 No Content'
LINKS_COUNT = 5