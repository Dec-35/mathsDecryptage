import time
import math
import random
from datetime import datetime
import string

#####################################################
#                       Arithmétique                #
#####################################################


def toBinary(a):
    return "".join(format(ord(x), "08b") for x in a)


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


def chiffreVigenere(mot, cle):
    motChiffre = ""
    for i in range(len(mot)):
        shift = code(
            cle[i % len(cle)]
        )  # Utilisation de la fonction code pour obtenir le décalage
        motChiffre += chiffreCesar(mot[i], shift)
    return motChiffre


def dechiffreVigenere(motChiffre, cle):
    motDechiffre = ""
    for i in range(len(motChiffre)):
        shift = code(
            cle[i % len(cle)]
        )  # Utilisation de la fonction code pour obtenir le décalage
        motDechiffre += dechiffreCesar(motChiffre[i], shift)
    return motDechiffre


def cleVernam(n):
    cle = ""
    for i in range(n):
        cle += chr(random.randint(0, 25) + 65)
    return cle


def chiffreVernam(mot):
    cle = cleVernam(len(mot))
    motChiffre = ""
    for i in range(len(mot)):
        shift = code(cle[i])
        motChiffre += chiffreCesar(mot[i], shift)
    return motChiffre, cle


def dechiffreVernam(motChiffre, cle):
    motDechiffre = ""
    for i in range(len(motChiffre)):
        shift = code(cle[i])
        motDechiffre += dechiffreCesar(motChiffre[i], shift)
    return motDechiffre


def printM(M):
    try:
        n = len(M)
        m = len(M[0])
    except:
        return print("")

    res = ""
    for i in range(n):
        for j in range(m):
            try:
                res += str(M[i][j])
            except:
                return print("")
            if j < m - 1:
                res += "\t"
        res += "\n"
    print(res)


# renvoie le résultat du produit de matrice
# Matrice vide en cas d'erreur
def prodMat(A, B):
    try:
        lA = len(A)
        cA = len(A[0])
        lB = len(B)
        cB = len(B[0])
    except:
        return dict()
    if cA != lB:
        return dict()

    res = dict()
    for i in range(lA):
        res[i] = dict()
        for j in range(cB):
            res[i][j] = 0
            for k in range(cA):
                res[i][j] += A[i][k] * B[k][j]
    return res


def cleHill():
    # la cle est une matrice A tq det(A) doit être inversible modulo 26
    # i.e. pgcd(ad-bc,26) = 1

    # on choisit une matrice aléatoire
    A = [[random.randint(0, 25) for i in range(2)] for j in range(2)]
    # on calcule le déterminant
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    # on vérifie que le déterminant est inversible modulo 26
    while pgcd(det, 26) != 1:
        A = [[random.randint(0, 25) for i in range(2)] for j in range(2)]
        det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return A


def chiffreHill(txt, cle):
    # on découpe le texte en blocs de 2 lettres
    blocs = [txt[i : i + 2] for i in range(0, len(txt), 2)]

    if len(blocs[-1]) == 1:
        blocs[-1] += "x"

    # on chiffre chaque bloc
    blocs_chiffres = []
    for bloc in blocs:
        # on transforme le bloc en matrice
        M = [[code(bloc[0])], [code(bloc[1])]]
        # on chiffre le bloc
        bloc_chiffre = prodMat(cle, M)
        # on transforme la matrice en bloc
        bloc_chiffre = chr(bloc_chiffre[0][0] % 26 + 65) + chr(
            bloc_chiffre[1][0] % 26 + 65
        )
        # on ajoute le bloc chiffré à la liste des blocs chiffrés
        blocs_chiffres.append(bloc_chiffre)

    # on retourne le texte chiffré
    return "".join(blocs_chiffres).lower()


def dechiffreHill(txt, cle):
    # on découpe le texte en blocs de 2 lettres
    blocs = [txt[i : i + 2] for i in range(0, len(txt), 2)]

    # on déchiffre chaque bloc
    blocs_dechiffres = []
    for bloc in blocs:
        # on transforme le bloc en matrice
        M = [[code(bloc[0])], [code(bloc[1])]]
        # on calcule l'inverse de la clé
        cle_inverse = invMat(cle)
        # on déchiffre le bloc
        bloc_dechiffre = prodMat(cle_inverse, M)
        # on transforme la matrice en bloc
        bloc_dechiffre = chr(bloc_dechiffre[0][0] % 26 + 65) + chr(
            bloc_dechiffre[1][0] % 26 + 65
        )
        # on ajoute le bloc déchiffré à la liste des blocs déchiffrés
        blocs_dechiffres.append(bloc_dechiffre)

    # on retourne le texte déchiffré
    return "".join(blocs_dechiffres).lower()


def hachage(x):
    # calculer h(x) -> h(x) = \sum_{i=0}^{l-1} x[i] \times 2^{l-i-1} \pmod{251}

    # convertir x en binaire
    bin = toBinary(x)
    # calculer la somme
    somme = 0
    for i in range(len(bin)):
        somme += int(bin[i]) * pow(2, len(bin) - i - 1)
    # calculer le modulo
    return somme % 251


def attaque_dico_hash(h, dic):
    dico = open(dic, mode="r")
    n = 0  # pour compter le nombre de mots
    t0 = datetime.now()  # l'heure à l'instant présent

    for mot in dico:
        n += 1
        mot = mot.strip()

        hash_mot = hash.sha256(mot.encode("utf-8")).hexdigest()
        if hash_mot == h:
            print("Le mot de passe est : ", mot)
            break

    print(
        "{} mot(s) ont étés testés en {} seconde(s),".format(
            n, (datetime.now() - t0).total_seconds()
        )
    )


## enregistrement du hash du mot de passe salé


def secure_password_generate(password):
    salt = "".join(random.choice(string.ascii_letters) for i in range(32))
    hashed_password = hash.sha256((password + salt).encode("utf-8")).hexdigest()
    return str(hashed_password) + "_" + str(salt)


def pertinence(phrase, arbre):
    pert = 0
    n = len(phrase)
    for i in range(n):
        test = True
        positionDico = arbre
        for j in range(i, n):
            cara = phrase[j]
            try:
                x = positionDico[cara]
            except:
                break
            if x["FINMOT"]:
                pert += 1
            positionDico = x
    return pert


def attaqueCesar(message):
    t0 = datetime.now()  # l'heure à l'instant présent
    n = 0  # pour compter le nombre de clés testées
    meilleur = 0  # meilleure pertinence
    meilleurTexte = ""
    meilleurCle = 0

    for cle in range(26):
        n += 1
        texte = dechiffreCesar(message, cle)

        if pertinence(texte, DICO_FR) > meilleur:
            meilleur = pertinence(texte, DICO_FR)
            meilleurTexte = texte
            meilleurCle = cle

    print(
        "{} clé(s) ont étés testées en {} seconde(s),".format(
            n, (datetime.now() - t0).total_seconds()
        )
    )
    return "Le meilleur message est : {} avec la clé {} et une pertinence de {}".format(
        meilleurTexte, meilleurCle, meilleur
    )


def attaqueAffine(message):
    t0 = datetime.now()  # l'heure à l'instant présent
    n = 0  # pour compter le nombre de clés testées
    meilleur = 0  # meilleure pertinence
    meilleurTexte = ""
    meilleurCle = 0

    for a in range(26):
        for b in range(26):
            n += 1
            texte = dechiffreAffine(message, a, b)

            if pertinence(texte, DICO_FR) > meilleur:
                meilleur = pertinence(texte, DICO_FR)
                meilleurTexte = texte
                meilleurCle = (a, b)

    print(
        "{} clé(s) ont étés testées en {} seconde(s),".format(
            n, (datetime.now() - t0).total_seconds()
        )
    )

    return "Le meilleur message est : {} avec la clé {} et une pertinence de {}".format(
        meilleurTexte, meilleurCle, meilleur
    )


def attaqueVigenere(message):
    t0 = datetime.now()  # l'heure à l'instant présent
    n = 0

    meilleur = 0  # meilleure pertinence
    meilleurTexte = ""
    meilleurCle = ""

    for k in range(1, 10):
        for cle in itertools.product(alphabet, repeat=k):
            n += 1
            texte = dechiffreVigenere(message, cle)

            if pertinence(texte, DICO_FR) > meilleur:
                meilleur = pertinence(texte, DICO_FR)
                meilleurTexte = texte
                meilleurCle = cle

    print(
        "{} mot(s) ont étés testés en {} seconde(s),".format(
            n, (datetime.now() - t0).total_seconds()
        )
    )

    return "{} avec la clé {} et une pertinence de {}".format(
        meilleurTexte, meilleurCle, meilleur
    )


def attaqueVigenere(message, maxSize):
    t0 = datetime.now()  # l'heure à l'instant présent
    n = 0

    meilleur = 0  # meilleure pertinence
    meilleurTexte = ""
    meilleurCle = ""

    for k in range(1, 10):
        for cle in itertools.product(alphabet, repeat=k):
            n += 1
            texte = dechiffreVigenere(message, cle)
            if n >= maxSize:
                print(
                    "{} mot(s) ont étés testés en {} seconde(s),".format(
                        n, (datetime.now() - t0).total_seconds()
                    )
                )

                return "{} avec la clé {} et une pertinence de {}".format(
                    meilleurTexte, meilleurCle, meilleur
                )

            if pertinence(texte, DICO_FR) > meilleur:
                meilleur = pertinence(texte, DICO_FR)
                meilleurTexte = texte
                meilleurCle = cle

    print(
        "{} mot(s) ont étés testés en {} seconde(s),".format(
            n, (datetime.now() - t0).total_seconds()
        )
    )

    return "{} avec la clé {} et une pertinence de {}".format(
        meilleurTexte, meilleurCle, meilleur
    )


def ic(texte):
    n = len(texte)
    alphabet = list(string.ascii_lowercase)
    somme = 0
    for lettre in alphabet:
        somme += texte.count(lettre) * (texte.count(lettre) - 1)
    return somme / (n * (n - 1))


def freq(txt):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    freq_table = [0] * 26  # Initialiser le tableau des fréquences

    for char in txt:
        if char in alphabet:
            index = alphabet.index(char)
            freq_table[index] += 1

    return freq_table


def maxFreq(txt):
    freq_table = freq(txt)
    max_freq = max(freq_table)
    index = freq_table.index(max_freq)
    return index


def attaqueFreqVigenere(txt, lg):
    t0 = datetime.now()
    n = 0
    # n is the number of words tested

    # On calcule les fréquences de chaque sous-texte
    freq_table = []
    for i in range(lg):
        freq_table.append(freq(txt[i::lg]))

    # On calcule les indices de coincidence de chaque sous-texte
    ic_table = []
    for i in range(lg):
        ic_table.append(ic(txt[i::lg]))

    # On calcule les décalages de chaque sous-texte

    decalage_table = []
    for i in range(lg):
        decalage_table.append(maxFreq(txt[i::lg]))

    # On calcule la clé
    cle = ""
    for i in range(lg):
        cle += chr(97 + (decalage_table[i] - 4) % 26)

    # On déchiffre le texte
    texte = dechiffreVigenere(txt, cle)

    print(
        "L'algorythme a pris {} seconde(s),".format(
            lg, (datetime.now() - t0).total_seconds()
        )
    )
    return "{} avec la clé partielle {}".format(texte, cle)


def rechercheTaillCle(txt):
    # use ic to find the best key length
    ic_list = []
    for i in range(1, 20):
        ic_list.append(ic(txt[i::i]))
    return ic_list.index(max(ic_list)) + 1
