import time 
import math
import random


#####################################################
#                       Arithmétique                #
#####################################################

def divEuclid1(a,b):
    q = 0
    r = a
    while r >= b:
        r = r-b
        q += 1
    return(q,r)

def divEuclid(a,b):
    q = 0
    r = a
    while (r >= b) | (r<0) :
        if r >= b:
            r = r-b
            q += 1
        else:
            r = r+b
            q -= 1
    return(q,r)

def pgcd_Euclide(a,b):
    r = [b, a%b]
    print(a," = ",b,"x",a//b," + ",a%b)
    i = 1
    while r[i] != 0:
        r.append(r[i-1]%r[i])
        print(r[i-1]," = ",r[i],"x",r[i-1]//r[i]," + ",r[i-1]%r[i])
        i += 1
    return r[i-1]

def pgcd(a,b):
    if a%b == 0:
        return b
    else:
        return pgcd(b,a%b)

def bezout(a,b):    
    if b == 0:
        return (1,0)
    else:
        (u,v) = bezout(b, a%b)
        q = a//b
        return (v, u - q*v)

def dioph(a,b,c):
    d = pgcdRec(a,b)
    if not c%d==0:
        print("pas de solution")
    else:
        a, b, c = a/d, b/d, c/d
        (x0,y0) = bezout(a,b)        
        return(x0*c,y0*c)

def invMod(a,n):
    if pgcd(a,n) != 1:
        print(a, " n'est pas inversible modulo ", n)
        return -1
    (u,v) = bezout(a,n)
    return u %n

def premiers(n):
    # doit retourner tous les nombres premiers inférieurs ou égaux à n en utilisant le crible d'Eratosthène
    liste = list(range(2,n+1))
    premiers = []
    while len(liste) != 0:
        p = liste[0]
        premiers.append(p)
        for k in liste:
            if k %p == 0:
                liste.remove(k)
    return premiers

def isPrime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n %2 == 0:
        return False
    k = 3
    while k <= math.sqrt(n):
        if n %k == 0:
            return False
        k += 2
    return True

def findPrimeFactor(n):
    # n est supposé ici non premier et >= 2
    if n %2 == 0:
        return 2
    k = 3
    while k <= math.sqrt(n):
        if n %k == 0:
            return k
        k += 2
    return -1
        
def decompPrime(n):
    liste = []
    while not isPrime(n):
        p = findPrimeFactor(n)
        liste.append(p)
        n = int(n/p)
    liste.append(n)
    return liste

#####################################################
#                       Crypto.                     #
#####################################################

