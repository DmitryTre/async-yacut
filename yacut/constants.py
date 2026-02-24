import os, string
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
ERROR_MISSING_REQUEST_BODY = 'Отсутствует тело запроса'
ERROR_INVALID_URL = 'Недопустимый URL: {url}'
ERROR_DUPLICATE_SHORT_ID = 'Короткая ссылка "{short}" уже существует'
ERROR_VALIDATION_FAILED = 'Ошибка валидации: {details}'
ERROR_RESERVED_SHORT_ID = 'ID "{short}" зарезервирован и не может быть использован'
ERROR_MISSING_REQUEST_BODY = 'Тело запроса не может быть пустым'
ERROR_MISSING_URL_FIELD = 'Обязательное поле "url" отсутствует'
ERROR_INVALID_SHORT_ID = 'Недопустимый формат ID. Используйте только строчные латинские буквы и цифры, максимум 16 символов'
ERROR_GENERATION_FAILED = 'Не удалось сгенерировать уникальную короткую ссылку после {attempts} попыток'
ERROR_SHORT_ID_NOT_FOUND = 'Короткая ссылка не найдена'

# Сообщения для валидации форм
MSG_FIELD_REQUIRED = 'Поле обязательно для заполнения'
MSG_URL_TOO_LONG = 'Ссылка слишком длинная (максимум {max_length} символов)'
MSG_SHORT_ID_TOO_LONG = 'Ссылка слишком длинная (максимум {max_length} символов)'
MSG_NO_FILES_SELECTED = 'Надо выбрать хотя бы один файл'
MSG_INVALID_SHORT_ID_CHARS = 'Короткий ID содержит недопустимые символы.'

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