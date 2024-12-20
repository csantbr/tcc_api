import base64
import binascii


class Base64Utils:
    """
    Utility class for Base64 encoding and decoding.
    """

    @staticmethod
    def decode(content: str) -> bytes:
        """
        Decode a Base64-encoded string.
        """
        try:
            return base64.b64decode(content)
        except binascii.Error as e:
            raise ValueError("Invalid Base64 content") from e

    @staticmethod
    def is_valid(content: str) -> bool:
        """
        Check if a string is valid Base64.
        """
        try:
            base64.b64decode(content)
            return True
        except binascii.Error:
            return False
