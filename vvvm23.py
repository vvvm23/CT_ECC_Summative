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
    k = len(m)

    if k < 1:
        return []

    r = 2
    while (1):
        if k > 2**r - r - 1:
            r += 1
        elif k < 2**r - r - 1:
            return []
        else:
            break

    G = np.array(hammingGeneratorMatrix(r))
    return (np.dot(m, G) % 2).tolist()

def hammingDecoder(v):
    k = len(v)
    r = 2
    while(1):
        if k > 2**r - 1:
            r += 1
        elif k < 2**r - 1:
            return []
        else:
            break

    m_i = 0
    G = np.array(hammingGeneratorMatrix(r))
    while m_i < 2**k - 1:
        m_b = decimalToVector(m_i, 2**r - r - 1)
        m_c = np.dot(m_b, G) % 2
        if hammingDistance(m_c, v) <= 1:
            return m_c
        else:
            m_i += 1

    return []

def messageFromCodeword(c):
    return []

def dataFromMessage(m):
    return []

def repetitionEncoder(m, n):
    R = np.array(repetitionGeneratorMatrix(n))
    return (np.outer(m, R).flatten() % 2).tolist()

def repetitionDecoder(v):
    # Does this need to decode vectors with multiple values in it?
    # Eg: 1100 = 10 rather than empty? 
    n = len(v)
    S = sum(v)
    if S > n / 2:
        return [1]
    elif S < n / 2:
        return [0]
    else:
        return []


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

def parityGeneratorMatrix(n):
    G = []
    for i in range(n - 1, -1, -1):
        G.append(decimalToVector(2**i, n) + [1])
    return G

def repetitionGeneratorMatrix(n):
    return [1]*n

def decimalToVector(n,r): 
    v = []
    for s in range(r):
        v.insert(0,n%2)
        n //= 2
    return v

def hammingDistance(m, v):
    return sum(list(map(lambda _: _[0] ^ _[1], list(zip(m,v)))))

print(hammingDecoder([1,1,0]))
print(hammingDecoder([1,0,0,0,0,0,0]))
print(hammingDecoder([0,1,1,0,0,0,0]))