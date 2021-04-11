from functools import lru_cache
import sys


def verify_prime(p):
    """
    Fermat's Little Theorem:
        If p is prime, x**(p-1) % p = 1 for all 0 < x < p
    """
    for x in range(2, p):
        if mod_power(x, p - 1, p) != 1:
            return False

    return True


def mod_power(x, d, n):
    """
    Computes x**d % n recursively.
    """

    if d == 0:
        return 1
    # d is even, recurse with d/2
    elif d % 2 == 0:
        z = mod_power(x, d / 2, n)
        return (z ** 2) % n
    # d is odd, strip off one x then recurse
    else:
        z = mod_power(x, (d - 1) / 2, n)
        return ((z ** 2) * x) % n


# This is effectively called twice with the same parameters
# So lru_cache will cache the most recent call
@lru_cache(maxsize=1)
def Euclid(a, b):
    """
    Returns (g,i,j) such that g is the gcd(a,b) and g = ai + bj
    """
    if b == 0:
        return (a, 1, 0)

    g, ihat, i = Euclid(b, a % b)
    j = ihat - (a // b) * i

    return (g, i, j)


def get_lowest_rel_prime(n):
    """
    Finds the lowest odd number relatively prime to n.
    """

    for i in range(3, n, 2):
        gcd, _, _ = Euclid(i, n)
        if gcd == 1:
            return i
    return -1


def write_key(value, n, fname):
    """Opens the file at fname and writes the key and n to it."""

    with open(
        fname,
        "w",
    ) as f:
        f.write("{0},{1}".format(value, n))


def keygen(p, q, verify=True):
    """
    Computes the public key P, secret key S, and size n
    such that for a given x, x**S % n gives an encrpyted value y and
    for a given y, y**P % n gives the original value x.

    Inputs:
    @param p: A prime number
    @param q: A different prime number
    @param verify: If True, p and q will be check. If either is composite,
    the function will throw an AssertionError.
    """
    if verify:
        # Verify primes
        print("Verifying inputs...")
        assert verify_prime(p) and verify_prime(q)
        print("Finished!")

    # Calculate P,S,mod
    n = p * q
    r = (p - 1) * (q - 1)

    # Select e relatively prime to r
    print("Scanning for relative prime...")
    e = get_lowest_rel_prime(r)
    print("Finished!")

    # compute d as multiplicative inverse of e: ed mod r = 1
    print("Computing multiplicative inverse...")
    _, _, j = Euclid(r, e)
    d = j % r
    print("Finished!")

    # Save to file
    P = e
    S = d

    print("Writing keys to files...")
    write_key(P, n, "public.key")
    write_key(S, n, "secret.key")
    print("Finished!")


if __name__ == "__main__":
    args = sys.argv

    if len(args) < 3 or len(args) > 4:
        print("Invalid number of arguments.")
        print(
            "Please provide p, q, and an optional verification flag to skip verification."
        )
        print("Ex: python3 rsa_keygen.py 11 19 False")

    # No 3rd argument
    if len(args) == 3:
        p = int(args[1])
        q = int(args[2])
        keygen(p, q)

    # 3rd argument
    if len(args) == 4:
        p = int(args[1])
        q = int(args[2])
        verify = args[3] == "True"
        keygen(p, q, verify)
