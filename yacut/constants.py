import os
import string

from settings import Config

# === КОНСТАНТЫ ПРИЛОЖЕНИЯ ===
SHORT_LEN = 16
SHORT = 6
ORIGINAL_LENGTH = 2048
MAX_GENERATION_ATTEMPTS = 100
VALID_CHARS = string.ascii_lowercase + string.digits
RESERVED_SHORT = {'files'}
INPUT_VALIDATION_REGEX = f'^[{VALID_CHARS}]*$'

DISK_TOKEN = os.getenv('DISK_TOKEN')


REQUEST_UPLOAD_URL = f'{Config.API_HOST}{Config.API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{Config.API_HOST}{Config.API_VERSION}/disk/resources/download'
HEADERS = {
    'Accept': 'application/json',
    'Authorization': f'OAuth {Config.DISK_TOKEN}'
}
BASE_URL = f'{Config.API_HOST}{Config.API_VERSION}/disk/resources/'
HREF_KEY_ERROR = 'Ключ href отсутствует.'
REDIRECT_ENDPOINT = 'redirect_to_url'
NO_CONTENT = 'API вернул статус 204 No Content'
LINKS_COUNT = 5
