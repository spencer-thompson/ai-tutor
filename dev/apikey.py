import base64
import os


def generate_key(length=32):
    """
    Generates API Keys at random
    """
    return base64.urlsafe_b64encode(os.urandom(length)).rstrip(b"=").decode("utf-8")


if __name__ == "__main__":
    print(generate_key())
