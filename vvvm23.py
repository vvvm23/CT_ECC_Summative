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

    # Try and make this into a nice one liner?
    out = []
    for x in range(2**r - 1):
        # if not sum(decimalToVector(x+1)) == 1
        if not m.log2(x+1) == m.floor(m.log2(x+1)): # If not power of 2 append to output
            out.append(c[x])

    return out

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
    if not valid_vector(m):
        return []
    # Get the outer product of m and repetition G matrix.
    # Then flatten to obtain code vector
    return (np.outer(m, np.array(repetitionGeneratorMatrix(n))).flatten() % 2).tolist()


# Decodes a repeated array into one bit
def repetitionDecoder(v):
    if not valid_vector(v):
        return []
    # Does this need to decode vectors with multiple values in it?
    # Eg: 1100 = 10 rather than empty? 

    return [1] if sum(v) > len(v) / 2 else [0] if sum(v) < len(v) / 2 else []

    '''n = len(v)
    S = sum(v)
    if S > n / 2: # If sum is greater than half of length then it was 1
        return [1]
    elif S < n / 2: # If sum is less than half of length then it was 0
        return [0]
    else: # If sum = half of length cannot determine
        return []'''

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
    H = []
    for i in range(1, 2**r): # Let rows be binary vectors from 1 to 2**r - 1
        H.append(decimalToVector(i, r))

    # Transform and return (or don't bother transforming to save time later)
    return np.array(H).T.tolist() 

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
def hammingDistance(m, v):
    # Creates list of tuples m and v and applies xor
    #..then sum resulting list to obtain distance
    return sum(list(map(lambda _: _[0] ^ _[1], list(zip(m,v)))))

def valid_vector(v):
    if type(v) != list:
        print("failing as not list")
        return False
    else:
        if len(v) == 0:
            print("failing as length 0")
            return False

        for _ in v:
            if not type(_) == int:
                print("failing as not int")
                return False
            if not _ in [0, 1]:
                print("failing as not binary")
                return False
            
    return True
'''print("Nuffin.")
print([1,0,0,1,1,0,1])
print(dataFromMessage(messageFromCodeword([1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1])))
print("\nFlip one bit")
print(dataFromMessage(messageFromCodeword(hammingDecoder([1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1]))))
print(dataFromMessage(messageFromCodeword(hammingDecoder([1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]))))
print(dataFromMessage(messageFromCodeword(hammingDecoder([1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1]))))
print("\nFlip two bits")
print(dataFromMessage(messageFromCodeword(hammingDecoder([1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1]))))
print(dataFromMessage(messageFromCodeword(hammingDecoder([1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1]))))
print(dataFromMessage(messageFromCodeword(hammingDecoder([1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1]))))
print(dataFromMessage(messageFromCodeword(hammingDecoder([1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1]))))
#print("[1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1]")
#print(dataFromMessage(messageFromCodeword(hammingDecoder([1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1]))))
#print("\n",dataFromMessage(messageFromCodeword(hammingDecoder([0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]))))
'''