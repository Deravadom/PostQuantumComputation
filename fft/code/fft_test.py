from fft_toys import getCoeff, evalPoly
from cmath import exp, pi
import sys


def pad_coeffs(a,b):
    """Pads two lists of coefficients to the length of
    the smallest power of 2 needed to 2n-2 items, where n is
    max(len(a), len(b)) 
    """
    #get  max length
    n = max(len(a), len(b))
    #get the number of bits required to hold the length
    shift = len(bin(n))-2

    #shift to get the next power of two
    #ex.: n=5, shift=3, next_power=8
    next_power = 1 << shift


    pad_a = next_power - len(a)
    pad_b = next_power - len(b)
    return (a + [0] * pad_a, b + [0]*pad_b)


TWO_PI_I = -2 * pi * 1j


def RFFT(a, exponent=TWO_PI_I):
    # region
    n = len(a)  # Always a power of 2

    # w_n^n is 1, so FFT of a single element is itself
    if n == 1:
        return a

    a_0 = a[0::2]
    a_1 = a[1::2]

    y_0, y_1 = RFFT(a_0, exponent), RFFT(a_1, exponent)

    w_n = exp(exponent / n)
    w = 1

    y = [0] * n
    # endregion
    for k in range(n // 2):
        left = y_0[k]
        right = w * y_1[k]

        y[k] = left + right
        y[k + n // 2] = left - right
        w = w * w_n

    return y


def IRFFT(y):
    # region
    n = len(y)
    return [item / n for item in RFFT(y, exponent=-TWO_PI_I)]


def fft_test(a, b, base=10, verbose=True):
    # Create coefficient representations of A an B as
    # degree-bound 2n polynomials (1/2)
    if verbose:
        print("Getting coefficients for base {0}:...".format(base))
    a_coeff, b_coeff = pad_coeffs(
        getCoeff(a,base), getCoeff(b,base)
    )
    if verbose:
        print("a:", a_coeff)
        print("b:", b_coeff)

    # Compute point-valued representations of A and B of length
    # 2n by applying the FFT of orer 2n on each.
    # These contain the valuees of the two polynomials at
    # the (2n)th roots of unity.
    if verbose:
        print("Performing fft...")
    a_fft = RFFT(a_coeff)
    b_fft = RFFT(b_coeff)

    if verbose:
        print("Values of a at the (2n)th roots of unity:\n", a_fft)
        print("Values of b at the (2n)th roots of unity:\n", b_fft)

    # Compute a point-value represention for c by multiplying
    # these values together piecewise
    multiplied = [x * y for x, y in zip(a_fft, b_fft)]
    if verbose:
        print("Multiplied values:\n", multiplied)

    # Create the coefficient representation of the polynomial c by
    # applying the FFT to compute the inverse DFT
    inverted = IRFFT(multiplied)
    if verbose:
        print("Result coefficients:\n", inverted)

    result = evalPoly(inverted, base)
    if verbose:
        print("Final multiplied value:", result)
    complex_result = complex(result)
    int_result = (complex_result.real**2+complex_result.imag**2)**.5
    if verbose:
        print("Integer result:", int(int_result))
    return int(int_result)

if __name__ == "__main__":
    args = sys.argv
    fft_test(int(args[1]), int(args[2]))
