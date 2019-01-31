import numpy as np
import math as m

# Converts from data to message format
def message(a):
    if not valid_vector(a):
        return []

    l = len(a)
    r_min = m.floor(m.log2(l)) + 1 # Calculates minimum r. Could just start with r=2?
    if r_min < 2:
        r_min = 2

    r = r_min
    while r + l > 2**r - r - 1: # Increments r until good value found
        r += 1

    l_b = decimalToVector(l, r)
    return l_b + a + [0] * (2**r - 2*r - 1 - l) # Appends length vector to message padded by 0s

# Converts message into hamming code
def hammingEncoder(m):
    if not valid_vector(m):
        return []

    k = len(m)
    if k < 1:
        return []

    r = 2
    while 1: # Increments r until valid r found
        if k > 2**r - r - 1:
            r += 1
        elif k < 2**r - r - 1:
            return []
        else:
            break

    G = np.array(hammingGeneratorMatrix(r))
    return (np.dot(m, G) % 2).tolist() # Calculates inner product between m and G

# Detects and corrects errors
def hammingDecoder(v):
    if not valid_vector(v):
        return []
    k = len(v)
    r = 2

    while 1: # Increment r until valid value found or failure
        if k > 2**r - 1:
            r += 1
        elif k < 2**r - 1:
            return []
        else:
            break

    H = np.array(parityGeneratorMatrix(r)) # Get parity matrix

    v_H = (np.dot(v, H.T) % 2).tolist() # Calculate v x H.T
    i = sum([v_H[j]*2**(r-j - 1) for j in range(r)]) # Get binary value

    if i == 0: # if no errors return v
        return v
    elif i > 2**r - 1: # if out of bounds return empty (not sure if possible)
        return []
    else:
        v[i-1] = (v[i-1] + 1) % 2 # Else, correct error
    return v
    
# Gets the message from the hamming code
def messageFromCodeword(c):
    if not valid_vector(c):
        return []
    r = 2
    k = len(c)
    while 1: # Increments r until valid r found
        if k > 2**r - 1:
            r += 1
        elif k < 2**r - 1:
            return []
        else:
            break

    return [c[x] for x in range(2**r - 1) if not sum(decimalToVector(x+1, r)) == 1]    


# Gets original data from message
def dataFromMessage(m):
    if not valid_vector(m):
        return []
    r = 2
    k = len(m)
    while 1: # Increment r until valid r found
        if k > 2**r - r - 1:
            r += 1
        elif k < 2**r - r - 1:
            return []
        else:
            break

    l_b = m[:r] # Slice message to get binary vector length
    l = 0
    for i in range(r): # Get decimal length
        l += l_b[i] * 2**(r-i-1)

    if sum(m[r+l:]) > 0 or l + r > k: 
        # If none zero encountered after message or calculated l+r
        #.. more than length return empty vector
        return []

    return m[r:r+l] # Return slice of message from r to r+l -> [r, r+l)

# Repetition encodes a message n times
def repetitionEncoder(m, n):
    return n*m if valid_vector(m) else []

# Decodes a repeated array into one bit
def repetitionDecoder(v):
    return ([1] if sum(v) > len(v) / 2 else [0] if sum(v) < len(v) / 2 else []) if valid_vector(v) else []

# Generates an r-hamming generator matrix
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

# Generates hamming parity matrix of size r
def parityGeneratorMatrix(r):
    return np.array([decimalToVector(i, r) for i in range(1, 2**r)]).T.tolist()

# Creates repetition generator matrix
def repetitionGeneratorMatrix(n):
    return [1]*n # Simply a vector of all 1s

# Converts n decimal number into binary vector
def decimalToVector(n,r): 
    v = []
    for s in range(r):
        v.insert(0,n%2)
        n //= 2
    return v

# Calculates hamming distance between m and v
# Legacy from brute force attempt
def hammingDistance(m, v):
    # Creates list of tuples m and v and applies xor
    #..then sum resulting list to obtain distance
    return sum(list(map(lambda _: _[0] ^ _[1], list(zip(m,v)))))

# Checks if vector conforms to input rules
def valid_vector(v):
    if type(v) != list: # if not a list then false
        print("failing as not list")
        return False
    else:
        if len(v) == 0: # if empty list then false
            return False

        for _ in v:
            if not type(_) == int: # if contains not int then false
                return False
            if not _ in [0, 1]: # if not binary then false
                return False
            
    return True # else true