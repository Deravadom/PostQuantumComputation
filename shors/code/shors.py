from qc import *
from fractions import Fraction


def c_amod15(a, power):
    """Controlled multiplication by a mod 15"""
    if a not in [2, 7, 8, 11, 13]:
        raise ValueError("'a' must be 2,7,8,11 or 13")
    U = QuantumCircuit(4)
    for iteration in range(power):
        if a in [2, 13]:
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
        if a in [7, 8]:
            U.swap(2, 3)
            U.swap(1, 2)
            U.swap(0, 1)
        if a == 11:
            U.swap(1, 3)
            U.swap(0, 2)
        if a in [7, 11, 13]:
            for q in range(4):
                U.x(q)
    U = U.to_gate()
    U.name = "%i^%i mod 15" % (a, power)
    c_U = U.control()
    return c_U


def guess_period(a):
    n_count = 8
    qc = QuantumCircuit(n_count + 4, n_count)

    # init counting registers to |+>
    for q in range(n_count):
        qc.h(q)

    # init aux register to |1>
    qc.x(3 + n_count)

    # perform C-Us
    for q in range(n_count):
        qc.append(c_amod15(a, 2 ** q), [q] + [i + n_count for i in range(4)])

    # inverse qft
    qft_dagger(qc, n_count)

    # measure
    qc.measure(range(n_count), range(n_count))

    # get r
    counts = simulate(qc)
    phases = [int(output, 2) / (2 ** n_count) for output in counts]
    guesses = [Fraction(phase).limit_denominator(15).denominator for phase in phases]
    return guesses


def shors15():
    N = 15
    # np.random.seed(1)
    # 1. Pick a random number 1<a<N
    a = np.random.randint(2, N - 1)
    print("Trying", a)
    # 2. Compute gcd(a,N)
    gcd_aN = np.gcd(a, N)
    # 3. If gcd(a,N) != 1, return a
    if not gcd_aN == 1:
        return a
    # 4. Else use quantum period finding function, r
    guesses = guess_period(a)
    print("Guesses:", guesses)
    # 4a. Multiple guesses
    for guess in guesses:
        # 5. If r is odd, re-run
        if guess % 2 == 1:
            continue
        half_guess = int(guess / 2)
        # 6. If a^(r/2) is congruent to -1 mod N, re-run
        if a ** (half_guess) % N == 14:
            continue

        # 7. Else gcd(a^(r/2)+1, N) and gcd(a^(r/2)-1, N) are nontrivial factors
        return [np.gcd((a ** half_guess) + 1, N), np.gcd((a ** half_guess) - 1, N)]

    # If we got here, re-try
    return shors15()
