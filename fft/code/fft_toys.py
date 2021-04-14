# Mark Boady
# Drexel University 2021


# https://medium.com/@aiswaryamathur/understanding-fast-fourier-transform-from-scratch-to-solve-polynomial-multiplication-8018d511162f

# If I have a really big number,
# I can treat it as coefficients of a polynomial
# If I evaluate it at the base, I get my number back
def getCoeff(num, base):
    L = []
    while num > 0:
        rem = num % base
        L.append(rem)
        num = num // base
    return L


# Undo by evaluating at point x
def evalPoly(coeff, x):
    res = 0
    for i in range(0, len(coeff)):
        res = res + coeff[i] * (x ** i)
    return res


# Make it pretty latex format
def prettyPoly(coeff):
    res = ""
    for i in range(0, len(coeff)):
        if coeff[i] != 0:
            if i == 0:
                res = res + str(coeff[i])
            else:
                res = res + str(coeff[i]) + "x^{" + str(i) + "}"
            if i + 1 < len(coeff):
                res = res + "+"
    if len(res) == 0:
        return "0"
    return res


# We can multiply using the polynomails
# As long as we evaluate at the right base, all will be well
def prod(f, g):
    fOrder = len(f)
    gOrder = len(g)
    # h=g*f
    hOrder = fOrder + gOrder - 1
    h = [0] * hOrder
    for j in range(0, hOrder):
        for k in range(0, j + 1):
            if k < fOrder and j - k < gOrder:
                h[j] += f[k] * g[j - k]
    return h


# We can normalize back to our base
def normalize(C, b):
    L = []
    quot = 0
    for i in range(0, len(C)):
        x = quot + C[i]
        rem = x % b
        quot = x // b
        L.append(rem)
    while quot > 0:
        rem = quot % b
        quot = quot // b
        L.append(rem)
    return L


# Normalized Product
def prodInt(x, y, b):
    myX = getCoeff(x, b)
    myY = getCoeff(y, b)
    H = prod(myX, myY)
    H = normalize(H, b)
    return evalPoly(H, b)


if __name__ == "__main__":
    b = 74
    number = 2918023894
    print("Initial Number:", number)
    C = getCoeff(number, b)
    print("Coefficents = ", C)
    print("Polynomial = ", prettyPoly(C))
    print("Number Eval =", evalPoly(C, b))

    # We can use base 2!
    b = 2
    print("Initial Number:", number)
    C = getCoeff(number, b)
    print("Coefficents = ", C)
    print("Polynomial = ", prettyPoly(C))
    print("Number Eval =", evalPoly(C, b))

    # Look it is binary
    b = 2
    number = 28
    print("Initial Number:", number)
    C = getCoeff(number, b)
    print("Coefficents = ", C)
    print("Polynomial = ", prettyPoly(C))
    print("Number Eval =", evalPoly(C, b))

    # Generate two numbers
    x = 240982308
    y = 198124098
    b = 74
    print("Goal:", x * y)

    Cx = getCoeff(x, b)
    print(prettyPoly(Cx))
    Cy = getCoeff(y, b)
    print(prettyPoly(Cy))
    Cz = prod(Cx, Cy)
    print(Cz)
    print("Number Eval =", evalPoly(Cz, b))
    print("Normalize")
    N = normalize(Cz, b)
    print(N)
    print("Number Eval =", evalPoly(N, b))
    print(getCoeff(x * y, b))

    # Basic Structure
    x = 19408230982039840298
    y = 238942098740932
    b = 2
    z = prodInt(x, y, b)
    print("Number Eval =", z)
    print("Goal        =", x * y)
