import numpy as np
import math as m

def message(a):
    l = len(a)
    r_min = m.floor(m.log2(l)) + 1
    if r_min < 2:
        r_min = 2

    r = r_min
    while r + l > 2**r - r - 1:
        r += 1

    l_b = decimalToVector(l, r)
    return l_b + a + [0] * (2**r - 2*r - 1 - l)

def hammingEncoder(m):
    pass

def hammingDecoder(v):
    pass

def messageFromCodeword(c):
    pass

def dataFromMessage(m):
    pass

def repetitionEncoder(m, n):
    pass

def repetitionDecoder(v):
    pass

def hammingGeneratorMatrix(r):
    n = 2**r-1
    
    #construct permutation pi
    pi = []
    for i in range(r):
        pi.append(2**(r-i-1))
    for j in range(1,r):
        for k in range(2**j+1,2**(j+1)):
            pi.append(k)

    #construct rho = pi^(-1)
    rho = []
    for i in range(n):
        rho.append(pi.index(i+1))

    #construct H'
    H = []
    for i in range(r,n):
        H.append(decimalToVector(pi[i],r))

    #construct G'
    GG = [list(i) for i in zip(*H)]
    for i in range(n-r):
        GG.append(decimalToVector(2**(n-r-i-1),n-r))

    #apply rho to get Gtranpose
    G = []
    for i in range(n):
        G.append(GG[rho[i]])

    #transpose    
    G = [list(i) for i in zip(*G)]

    return G

def decimalToVector(n,r): 
    v = []
    for s in range(r):
        v.insert(0,n%2)
        n //= 2
    return v

print(message([1]))
print(message([0,0,1]))
print(message([0,1,1,0]))
print(message([1,1,1,1,0,1]))