import os
import string

from settings import Config

# === КОНСТАНТЫ ПРИЛОЖЕНИЯ ===
SHORT_LEN = 16
CUSTOM_SHORT = 6
ORIGINAL_LENGHT = 2048
MAX_GENERATION_ATTEMPTS = 100
VALID_CHARS = (string.ascii_lowercase + string.digits)
RESERVED_IDS = {'/files', '/admin', '/api'}

DISK_TOKEN = os.getenv('DISK_TOKEN')
YA_CUT_PATH_PREFIX = '/ya_cut/'
REDIRECT_VIEW_NAME = 'redirect_to_url'

# === КОНСТАНТЫ СООБЩЕНИЙ ОБ ОШИБКАХ (уровень модуля) ===
ERROR_MISSING_REQUEST_BODY = 'Тело запроса пустое'
ERROR_INVALID_URL = 'Недопустимый URL: {url}'
ERROR_DUPLICATE_SHORT_ID = 'Короткая ссылка "{short}" занята'
ERROR_VALIDATION_FAILED = 'Ошибка валидации: {details}'
ERROR_RESERVED_SHORT_ID = 'ID "{short}" зарезервирован'
ERROR_MISSING_URL_FIELD = 'Поле "url" отсутствует'
ERROR_INVALID_SHORT_ID = 'Недопустимый ID. Только a-z, 0-9, до 16 симв.'
ERROR_GENERATION_FAILED = 'Не удалось сгенерировать после {attempts} попыток'
ERROR_SHORT_ID_NOT_FOUND = 'Короткая ссылка не найдена'
ERROR_DOWNLOAD_LINK = 'Ошибка получения ссылки для загрузки'

# Сообщения для валидации форм
MSG_FIELD_REQUIRED = 'Поле обязательно для заполнения'
MSG_URL_TOO_LONG = 'Ссылка длиннее {max_length} символов'
MSG_SHORT_ID_TOO_LONG = 'ID длиннее {max_length} символов'
MSG_NO_FILES_SELECTED = 'Выберите хотя бы один файл'
MSG_INVALID_SHORT_ID_CHARS = 'Недопустимые символы в ID'

# Подписи полей форм
LABEL_ORIGINAL_LINK = 'Оригинальная ссылка'
LABEL_CUSTOM_ID = 'Ваш вариант короткой ссылки'
LABEL_FILES = 'Выберите файлы для загрузки'

# Надписи кнопок
LABEL_SUBMIT_SHORTEN = 'Создать'
LABEL_SUBMIT_UPLOAD = 'Загрузить файлы'

# Успешные ответы (2xx)
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204

# Перенаправления (3xx)
HTTP_301_MOVED_PERMANENTLY = 301
HTTP_302_FOUND = 302
HTTP_304_NOT_MODIFIED = 304

# Клиентские ошибки (4xx)
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404

# Серверные ошибки (5xx)
HTTP_500_INTERNAL_SERVER_ERROR = 500

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
HEADERS = {
    'Accept': 'application/json',
    'Authorization': f'OAuth {Config.DISK_TOKEN}'
}
HREF_KEY_ERROR = 'Ключ href отсутствует.'