# -*- coding: utf-8 -*-
"""
Created on Mon May 18 10:37:09 2020

@author: edinh
"""
from math import sqrt

import time
def lsqrt(n):
  x = n
  y = (x + n // x) // 2
  while y < x:
    x = y
    y = (x + n // x) // 2
  return x

def estpremier(n):
    """estpremier(n): dit si un nombre est premier (renvoie True ou False)"""
    if n<7:
        if n in (2,3,5):
            return True
        else:
            return False
    # si n est pair et >2 (=2: cas traité ci-dessus), il ne peut pas être premier
    if n & 1 == 0:
        return False
    # autres cas
    k=3
    r=lsqrt(n)
    while k<=r:
        if n % k == 0:
            return False
        k+=2
    return True
##############################################################################
def lrac(x):
    """Racine carrée entière d'un nb entier x (méth. de Héron d'Alexandrie)"""
    r1 = 1
    while True:
        r2 = (r1+x//r1)//2 
        if abs(r1-r2) < 2:
            if r1*r1 <= x and (r1+1)*(r1+1) > x:
                return r1
        r1 = r2
 
##############################################################################
def pgcd(a,b):
    """Calcul du 'Plus Grand Commun Diviseur' de a et b entiers (Euclide)"""
    while b:
        a, b = b, a%b
    return a
 
##############################################################################
def facteursdiv2(n):
    """Décomposition par division de n (entier) en 2 facteurs quelconques"""
    pp = [2, 3, 5, 7, 11]
    racn = lrac(n)+1  # lrac(n) = racine carrée entière de n
    for p in pp:
        if p>racn:
            return [n, 1]  # n est premier
        if n%p == 0:
            return [p, n//p]  # on a trouvé une décomposition
    p = pp[-1] + 2
    while p <= racn:
        if n%p == 0:
            return [p, n//p]  # on a trouvé une décomposition
        p += 2
    # si on arrive ici, n est premier
    return [n, 1]
 
#############################################################################
def pollardrho(n):
    """Factorisation d'un nombre entier décomposable (méth. rho de pollard)"""   
    f = lambda z: z*z+1
    x, y, d = 2, 2, 1
    while d==1:
        x = f(x) % n
        y = f(f(y)) % n
        d = pgcd(x-y, n)
    return [d, n//d]
 
##############################################################################
def fermat(n, verbose=True):
    if n%2==0:
        return [2,int(n/2)]
    a = lsqrt(n) # int(ceil(n**0.5))
    b2 = a*a - n
    b = lsqrt(n) # int(b2**0.5)
    count = 0
    while b*b != b2:
        #if verbose:
            #print('Trying: a=%s b2=%s b=%s' % (a, b2, b))
        a = a + 1
        b2 = a*a - n
        b = lsqrt(b2) # int(b2**0.5)
        count += 1
    p=a+b
    q=a-b
    assert n == p * q
    #print('a=',a)
    #print('b=',b)
    #print('p=',p)
    #print('q=',q)
    #print('pq=',p*q)
    return [p, q]   


##############################################################################

def Pfactpremiers(n):
    #liste des facteurs premiers de n, avec la fonction 'a, b = decomp(n)' 
    R = []  # liste des facteurs premiers trouvés
    P = [n]  # pile de calcul
    while P!=[]:
        x = P.pop(-1)  # lecture et dépilage de la dernière valeur empilée
        if estpremier(x):
            R.append(x)  # on a trouvé un facteur 1er => on ajoute à la liste
        else:
            a, b = pollardrho(x)  # on calcule une nouvelle décomposition
            if a==1 or b==1:
                # echec: x n'est pas 1er mais sa decomposition ne se fait pas
                # on essaie une décomposition par division
                a, b = facteursdiv2(x)
            P.append(a)  # on empile a
            P.append(b)  # on empile b
    R.sort()
    return R

def Ffactpremiers(n):
    #liste des facteurs premiers de n, avec la fonction 'a, b = decomp(n)' 
    R = []  # liste des facteurs premiers trouvés
    P = [n]  # pile de calcul
    while P!=[]:
        x = P.pop(-1)  # lecture et dépilage de la dernière valeur empilée
        if estpremier(x):
            R.append(x)  # on a trouvé un facteur 1er => on ajoute à la liste
        else:
            a, b = fermat(x)  # on calcule une nouvelle décomposition
            if a==1 or b==1:
                # echec: x n'est pas 1er mais sa decomposition ne se fait pas
                # on essaie une décomposition par division
                a, b = facteursdiv2(x)
            P.append(a)  # on empile a
            P.append(b)  # on empile b
    R.sort()
    return R

def trivial(n):
    nb=n
    i=1
    l=[]
    rac = int(sqrt(n))+1
    while nb != 1 and i != rac :
        i=i+1
        if nb%i == 0 :
            nb=nb/i
            l.append(i)
            i=i-1
    l.append(nb)
    return(l)  
    
def main():
    print("Voici la simulation de factorisation des grands nombres faite par le groupe G1D")
    print("Nous avons trois algos, un trivial qui tente de diviser le nombre N par tous ceux inférieur à la racine carré de N")
    print("Un algo basé sur celui de Pollard Rho")
    print("Un algo basé sur celui de Fermat")
    print("""Si vous dépassez dix chiffres, ça risque de prendre un peu de temps :)""")
    while True:
        print("")
        print("Veuillez entrez un nombre puis appuyer sur la touche Entrée")
        n=int(input())
        print("Le programme s'exécute")
        print("")
        
        start_time1 = time.perf_counter()
        T=trivial(n)
        end_time1=time.perf_counter()-start_time1
        print("la liste de facteurs obtenus avec l'algo trivial est :",T)
        print("L'éxecution avec le programme trivial a pris",end_time1,"secondes")
        
        start_time2 = time.perf_counter()
        P=Pfactpremiers(n)
        end_time2=time.perf_counter()-start_time2
        print("la liste de facteurs obtenus avec l'algo de pollard est :",P)
        print("L'éxecution avec l'algo de pollard a pris",end_time2,"secondes")
        
    
        start_time3 = time.perf_counter()
        F=Ffactpremiers(n)
        end_time3=time.perf_counter()-start_time3
        print("la liste de facteurs obtenus avec l'algo de fermat est :",F)
        print("L'éxecution avec l'algo de fermat a pris",end_time3,"secondes") 
        
main()
          