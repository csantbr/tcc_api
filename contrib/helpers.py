import base64
import binascii

from contrib.exceptions import InvalidContent, InvalidLanguageType


def valid(language):
    if language not in ['py', 'c', 'cpp']:
        raise InvalidLanguageType(field='language_type')


def decode(content):
    if not content:
        raise InvalidContent(field='content')

    try:
        code = base64.b64decode(content)
    except binascii.Error:
        raise InvalidContent(field='content')

    return code
