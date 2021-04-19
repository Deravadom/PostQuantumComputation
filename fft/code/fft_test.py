from fft_toys import getCoeff, evalPoly
from cmath import exp, pi
from math import pow, sqrt
import sys
from numpy.fft import fft, ifft


def pad_coeffs(a, b):
    """
    Given two coefficient arrays of max length n, the resulting arrays are
    padded to the lowest power of 2 greater than 2n-1.
    """
    # get  max length
    n = max(len(a), len(b))
    # get the number of bits required to hold the length
    #bin(n) => '0bxxxx'
    n = 2*n-1
    shift = len(bin(n)) - 2

    # shift to get the next power of two
    # ex.: n=5, shift=3, next_power=8
    next_power = 1 << shift

    pad_a = next_power - len(a)
    pad_b = next_power - len(b)

    res_a = a + [0]*pad_a
    res_b = b + [0]*pad_b
    return res_a, res_b


TWO_PI_I = -2 * pi * 1j


def RFFT(a, exponent=TWO_PI_I):
    """Performs a recurssive fast-Fourier transform."""

    # region
    n = len(a)  # Always a power of 2

    # w_n^n is 1, so FFT of a single element is itself
    if n == 1:
        return a


    #split a into even and odd elements
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
    """Performs an inverse, recursive fast-Fourier transform."""

    n = len(y)
    return [item / n for item in RFFT(y, exponent=-TWO_PI_I)]


def fft_test(a, b, base=10, verbose=True):
    # Create coefficient representations of A an B as
    # degree-bound 2n polynomials (1/2)
    if verbose:
        print("Getting coefficients for base {0}:...".format(base))
    a_coeff, b_coeff = pad_coeffs(getCoeff(a, base), getCoeff(b, base))
    if verbose:
        print("a:", a_coeff)
        print("b:", b_coeff)
        print("lengths", len(a_coeff), len(b_coeff))

    # Compute point-valued representations of A and B of length
    # 2n by applying the FFT of orer 2n on each.
    # These contain the valuees of the two polynomials at
    # the (2n)th roots of unity.
    if verbose:
        print("Performing fft...")
    a_fft = RFFT(a_coeff)
    b_fft = RFFT(b_coeff)

    a_fft_numpy = fft(a_coeff)
    b_fft_numpy = fft(b_coeff)
    if verbose:
        print("Values of a at the (2n)th roots of unity:\n", a_fft)
        print("Values of b at the (2n)th roots of unity:\n", b_fft)
        print("According to numpy, a is:\n", a_fft_numpy)
        print("According to numpy, b is:\n", b_fft_numpy)

    # Compute a point-value represention for c by multiplying
    # these values together piecewise
    # multiplied = [x * y for x, y in zip(a_fft, b_fft)]
    multiplied = []
    for i in range(min(len(a_fft_numpy), len(b_fft_numpy))):
        multiplied.append(a_fft_numpy[i]*b_fft_numpy[i])

    if verbose:
        print("Multiplied values:\n", multiplied)

    # Create the coefficient representation of the polynomial c by
    # applying the FFT to compute the inverse DFT
    inverted = IRFFT(multiplied)
    numpy_inverted = ifft(multiplied)
    if verbose:
        print("Result coefficients:\n", inverted)
        print("According to numpy, a is:\n", numpy_inverted)

    result = evalPoly(inverted, base)
    if verbose:
        print("Final multiplied value:", result)
        print("Numpy's result:", evalPoly(numpy_inverted, base))
    complex_result = complex(result)
    int_result = (complex_result.real ** 2 + complex_result.imag ** 2) ** 0.5
    if verbose:
        print("Integer result:", int(int_result))
    return int(int_result)


if __name__ == "__main__":
    args = sys.argv
    fft_test(int(args[1]), int(args[2]))
