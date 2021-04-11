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
    """Returns value**key % n."""
    return mod_power(value, key, n)


def encode(text):
    """Converts a string to the base64 encoding of its ascii values."""
    return b64encode(text.encode())


def decode(text):
    """Converts a base64 encoding of ascii values back to a string."""
    return b64decode(text).decode()


def num_to_padded_ascii(num, max_len, base=256):
    """
    Calculates the digits of `num` in base `base` and
    converts to a padded string. 
    Note: To work properly, this must be true: num < base**(max_len-1).

    Ex: `num_to_padded_ascii(45, 4, 4)`\\
    45 =  2*(4**2) + 3*(4**1) + 1*(4**0)\\
    45 in base 4 = 231\\
    result: 0231
    """
    result = ""
    while num > 0:
        # grab first digit
        digit = num % base
        # add char value to result
        result += chr(digit)
        # remove digit
        num = num // base

    # check if padding needed
    if len(result) < max_len:
        # calculate how much is needed
        pad_size = max_len - len(result)
        # apply pad
        result += chr(0) * pad_size

    # Grabbing digits yields the reversed number
    # So reverse it back
    return result[::-1]


def padded_ascii_to_num(word, base=256):
    """
    Converts a string to an integer where the unicode values
    of the string represent digits in the given base `base`.
    """
    size = len(word)
    return sum([ord(char) * base ** i for i, char in enumerate(word[::-1])])


def encrypt_text(text, key, n):
    """
    Encrypts a body of text and encodes in base64.
    """
    # Encode as ascii values
    encoded = text.encode()
    # Encrypt each ascii value
    encrypted = [encrypt(i, key, n) for i in encoded]
    # Calculate allocated size using the size of n in base 256
    max_len = len(num_to_padded_ascii(n, 0))
    converted = [num_to_padded_ascii(i, max_len) for i in encrypted]
    # Encode string as base64 bytes
    return encode("".join(converted))


def decrypt_text(text, key, n):
    """
    Converts a body of encrypted, base64 text back
    to string format.
    """
    # Decode to padded ascii
    decoded = decode(text)
    # Calculate word size
    word_size = len(num_to_padded_ascii(n, 0))
    # Split into words
    words = [decoded[i : i + word_size] for i in range(0, len(decoded), word_size)]
    # Convert each word to unicode value
    codes = [padded_ascii_to_num(word) for word in words]
    # Decrypt each code
    decrypted = [encrypt(code, key, n) for code in codes]
    # Convert unicode back to string
    return "".join([chr(value) for value in decrypted])


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
