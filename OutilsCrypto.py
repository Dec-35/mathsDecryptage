import time
import math
import random


#####################################################
#                       Arithmétique                #
#####################################################


def divEuclid1(a, b):
    q = 0
    r = a
    while r >= b:
        r = r - b
        q += 1
    return (q, r)


def divEuclid(a, b):
    q = 0
    r = a
    while (r >= b) | (r < 0):
        if r >= b:
            r = r - b
            q += 1
        else:
            r = r + b
            q -= 1
    return (q, r)


def pgcd_Euclide(a, b):
    r = [b, a % b]
    print(a, " = ", b, "x", a // b, " + ", a % b)
    i = 1
    while r[i] != 0:
        r.append(r[i - 1] % r[i])
        print(r[i - 1], " = ", r[i], "x", r[i - 1] // r[i], " + ", r[i - 1] % r[i])
        i += 1
    return r[i - 1]


def pgcd(a, b):
    if a % b == 0:
        return b
    else:
        return pgcd(b, a % b)


def bezout(a, b):
    if b == 0:
        return (1, 0)
    else:
        (u, v) = bezout(b, a % b)
        q = a // b
        return (v, u - q * v)


def dioph(a, b, c):
    d = pgcdRec(a, b)
    if not c % d == 0:
        print("pas de solution")
    else:
        a, b, c = a / d, b / d, c / d
        (x0, y0) = bezout(a, b)
        return (x0 * c, y0 * c)


def invMod(a, n):
    if pgcd(a, n) != 1:
        print(a, " n'est pas inversible modulo ", n)
        return -1
    (u, v) = bezout(a, n)
    return u % n


def premiers(n):
    # doit retourner tous les nombres premiers inférieurs ou égaux à n en utilisant le crible d'Eratosthène
    liste = list(range(2, n + 1))
    premiers = []
    while len(liste) != 0:
        p = liste[0]
        premiers.append(p)
        for k in liste:
            if k % p == 0:
                liste.remove(k)
    return premiers


def isPrime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    k = 3
    while k <= math.sqrt(n):
        if n % k == 0:
            return False
        k += 2
    return True


def findPrimeFactor(n):
    # n est supposé ici non premier et >= 2
    if n % 2 == 0:
        return 2
    k = 3
    while k <= math.sqrt(n):
        if n % k == 0:
            return k
        k += 2
    return -1


def decompPrime(n):
    liste = []
    while not isPrime(n):
        p = findPrimeFactor(n)
        liste.append(p)
        n = int(n / p)
    liste.append(n)
    return liste


#####################################################
#                       Crypto.                     #
#####################################################
def Filtre(txt):
    res = ""
    for c in txt.lower():
        if ord("a") <= ord(c) <= ord("z"):
            res += c
        if c == "à" or c == "â" or c == "ä" or c == "á" or c == "å":
            res += "a"
        elif c == "ç":
            res += "c"
        elif c == "é" or c == "è" or c == "ê" or c == "ë":
            res += "e"
        elif c == "ï" or c == "î" or c == "ì" or c == "í":
            res += "i"
        elif c == "ö" or c == "ò" or c == "ô" or c == "ø" or c == "ó":
            res += "o"
        elif c == "û" or c == "ü" or c == "ù" or c == "ú":
            res += "u"
        elif c == "æ":
            res += "ae"
        elif c == "œ":
            res += "oe"
        elif c == "ÿ":
            res += "y"
        elif c == "ñ":
            res += "n"
        elif c == "ß":
            res += "ss"
    return res


def code(c):
    res = ""
    res = Filtre(c)
    if res == "":
        return -1

    return ord(res) - 97  # décalage unicode


def decode(n):
    # à compléter
    if 0 <= n <= 25:
        n = n + 97
        return chr(n)
    return "?"


def chiffreCesar(mot, k):
    res = ""
    for c in mot:
        res += decode((code(c) + k) % 26)
    return res


def dechiffreCesar(mot, k):
    res = ""
    for c in mot:
        res += decode((code(c) - k) % 26)
    return res


def chiffreAffine(mot, a, b):
    # a * mot + b

    res = ""
    for c in mot:
        res += decode((a * code(c) + b) % 26)
    return res


def dechiffreAffine(mot, a, b):
    # cas impossible
    if invMod(a, 26) == -1:
        return "Impossible"

    res = ""
    for c in mot:
        res += decode((invMod(a, 26) * (code(c) - b)) % 26)
    return res


def invMat(mat):
    a, b = mat[0][0], mat[0][1]
    c, d = mat[1][0], mat[1][1]

    det = a * d - b * c

    # Vérifier si la matrice est inversible
    if det == 0:
        raise ValueError("La matrice n'est pas inversible")

    # Calcul de l'inverse modulo 26
    det_inv = pow(det, -1, 26)

    # Calcul de la matrice inverse
    inv_a = (d * det_inv) % 26
    inv_b = (-b * det_inv) % 26
    inv_c = (-c * det_inv) % 26
    inv_d = (a * det_inv) % 26

    return [[inv_a, inv_b], [inv_c, inv_d]]
