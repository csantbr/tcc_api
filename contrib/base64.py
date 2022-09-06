import base64
import binascii

from contrib.exceptions import InvalidBase64


def decode(content):
    try:
        code = base64.b64decode(content)
    except binascii.Error:
        raise InvalidBase64

    return code
