from rsa_keygen import mod_power
from base64 import b64encode, b64decode
import sys


def read_key_info(keyname):
    """
    Reads the file at keyname. The file is assumed to
    have the structure: key,n.
    """
    with open(keyname, "r") as f:
        key, n = f.read().split(",")
    return int(key), int(n)


def encrypt(value, key, n):
    return mod_power(value, key, n)


def encode(text):
    return b64encode(text.encode())


def decode(text):
    return b64decode(text).decode()


def encrypt_text(text, key, n):
    """
    Encrypts a body of text and encodes in base64.
    """
    encoded = text.encode()
    encrypted = [encrypt(i, key, n) for i in encoded]
    result = encode("".join([chr(i) for i in encrypted]))
    return result


def decrypt_text(text, key, n):
    """
    Converts a body of encrypted, base64 text back
    to string format.
    """
    ords = [ord(i) for i in decode(text)]
    decrypted = [encrypt(i, key, n) for i in ords]
    result = "".join([chr(i) for i in decrypted])
    return result


def encrypt_or_decrypt_file(filename, keyname, encrypted, resultname):
    read_format, write_format, func = (
        ("rb", "w", decrypt_text) if encrypted == True else ("r", "wb", encrypt_text)
    )
    with open(filename, read_format) as f:
        text = f.read()

    key, n = read_key_info(keyname)
    result = func(text, key, n)

    with open(resultname, write_format) as f:
        f.write(result)


if __name__ == "__main__":
    args = sys.argv

    filename = args[1]
    keyname = args[2]
    encrypted = args[3] == "True"
    resultname = args[4]

    encrypt_or_decrypt_file(filename, keyname, encrypted, resultname)
