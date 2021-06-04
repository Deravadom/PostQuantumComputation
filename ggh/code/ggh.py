import numpy as np
from base64 import b64encode, b64decode
from math import sqrt
import sys

# Encryption
# Given a message m=(m_1,...,m_n), error e, and a public key B', compute
# v = sum(m_i*b'_i)
# v = m_i dot b_i
def encrypt(m, e, B_prime):
    return np.dot(m, B_prime) + e


# Decryption
# c dot B^-1 = (m dot B' + e)B^-1 = m dot U dot B dot B^-1 + e dot B^-1 = m dot U + e dot B^-1
# Babai round technique used to remove sufficiently small term e dot B^-1
# compute m = m dot U dot U ^-1
def decrypt(m, U_inv, B_inv):
    cb_inv = np.dot(m, B_inv)
    rounded = np.around(cb_inv, 0)
    return np.dot(rounded, U_inv)


def encode(message):
    """Encodes a message in base 64"""
    return b64encode(message.encode())


def decode(message):
    """Decodes a b64 string to ascii values"""
    return b64decode(message.encode())


def to_pairs(A):
    """Given a list A of even length, returns a list of pairs
    where each pair is [A[i], A[i+1]]. Throws an assertion error if A is of odd length.
    """
    assert len(A) % 2 == 0
    return [[A[i], A[i + 1]] for i in range(0, len(A), 2)]


def flatten(A):
    """Flattens an N-dimensional array into a 1-dimensional array"""
    return list(np.asarray(A).flat)


def encrypt_text(text, e, B_prime):
    # 1. check length, buffer and flag if odd
    message = text if len(text) % 2 == 0 else chr(0) + text
    # 2. encode, b64encode
    encoded = encode(message)
    # 3. split into pairs and encrypt
    pairs = to_pairs(encoded)
    encrypted = [encrypt(pair, e, B_prime) for pair in pairs]
    # 4. convert each pair value into b256
    converter = lambda x: [x[0] // 256, x[0] % 256, x[1] // 256, x[1] % 256]
    converted = [converter(e) for e in encrypted]
    # 5. flatten
    flattened = flatten(converted)
    # 6. stringify
    #potential problen
    stringified = [chr(int(c)) for c in flattened]
    # 5. encode
    cyphertext = "".join(stringified)
    return encode(cyphertext).decode()


def decrypt_text(text, U_inv, B_inv):
    # 1. double decode
    decoded = decode(text).decode()
    # 2. get pairs
    pairs = to_pairs(decoded)
    # 3. convert pairs to ascii values
    pairs = [[ord(p[0]), ord(p[1])] for p in pairs]
    # 4. convert pairs from b256 to single b10 value
    converter = lambda x: x[0] * 256 + x[1]
    converted = [converter(pair) for pair in pairs]
    # 5. get pairs
    pairs = to_pairs(converted)
    # 6. decrypt each pair
    decrypted = [decrypt(pair, U_inv, B_inv) for pair in pairs]
    # 7. flatten
    flattened = flatten(decrypted)
    # 8. stringifiy
    stringified = "".join([chr(int(value)) for value in flattened])
    # 9. double decode
    decoded = decode(stringified).decode()
    # 10. check for extra character
    extra = chr(0)
    return decoded[1:] if decoded[0] == extra else decoded

def generate_key_files():
    B = [[7, 0], [0, 3]]
    B_inv = [[1 / 7, 0], [0, 1 / 3]]
    U = [[2, 3], [3, 5]]
    U_inv = [[5, -3], [-3, 2]]
    B_prime = np.dot(U, B)
    B_prime = [list(b) for b in B_prime]
    e = [1, -1]

    with open("public.key", 'w') as f:
        #structure: b_00 b_01 b_10 b_11,e_00 e_01
        b_flat = flatten(B_prime)
        b_str = [str(x) for x in b_flat]
        e_str = [str(x) for x in e]

        f.write(f"{' '.join(b_str)},{' '.join(e_str)}")

    
    with open("secret.key", 'w') as f:
        #structure: b_00 b_01 b_10 b_11,u_00 ...
        b_flat = flatten(B_inv)
        u_flat = flatten(U_inv)

        b_str = [str(x) for x in b_flat]
        u_str = [str(x) for x in u_flat]

        f.write(f"{' '.join(b_str)},{' '.join(u_str)}")

def read_key(keyname):
    with open(keyname) as f:
        keys = f.read().split(',')

    b = [float(c) for c in keys[0].split()]
    other = [float(c) for c in keys[1].split()]
    dim = int(sqrt(len(b)))

    b_key = [b[dim*i:dim*(i+1)] for i in range(dim)]
    if len(other) == dim:
        return b_key,other
    else:
        u = [other[dim*i:dim*(i+1)] for i in range(dim)]
        return b_key,u


def main():
    #args: [encrypt|decrypt] fname keyname
    args = sys.argv
    action, fname, keyname = args[1:]

    with open(fname) as f:
        text = f.read()

    keys = read_key(keyname)

    if action == "encrypt":
        cyphertext = encrypt_text(text, keys[1], keys[0])
        with open("cyphertext.txt", 'w') as f:
            f.write(cyphertext)

    if action == "decrypt":
        recovered = decrypt_text(text, keys[1], keys[0])
        with open("decrypted.txt", 'w') as f:
            f.write(recovered)


if __name__ == "__main__":
    main()
