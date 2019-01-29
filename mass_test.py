from vvvm23 import *
import random

nb_test_one = 1000
nb_test_two = 10
nb_test_three = 10

# Test of full cycle with no bit changes #
r = m.floor(m.log2(nb_test_one)) + 1
for i in range(nb_test_one):
    print("Testing:", i)
    c = decimalToVector(i, r)
    assert c == dataFromMessage(messageFromCodeword(hammingDecoder(hammingEncoder(message(c)))))

# Test of full cycle with one bit change #
r = m.floor(m.log2(nb_test_two)) + 1
for i in range(nb_test_two):
    c = decimalToVector(i, r)
    c_h = hammingEncoder(message(c))
    j = random.randint(0, len(c_h) - 1)
    print("Testing:", i,"; Flipping:", j)
    c_h[j] = (c_h[j] + 1) % 2
    c_d = dataFromMessage(messageFromCodeword(hammingDecoder(c_h)))
    print("Original:",c,"; Mid:", c_h,"; End:",c_d,"\n")

# Test of full cycle with two bit changes #
r = m.floor(m.log2(nb_test_two)) + 1
for i in range(nb_test_two):
    c = decimalToVector(i, r)
    c_h = hammingEncoder(message(c))
    j = random.sample(range(len(c_h) - 1), 2)
    print("Testing:", i,"; Flipping:", j[0], j[1])
    c_h[j[0]] = (c_h[j[0]] + 1) % 2
    c_h[j[1]] = (c_h[j[1]] + 1) % 2
    c_d = dataFromMessage(messageFromCodeword(hammingDecoder(c_h)))
    print("Original:",c,"; Mid:", c_h,"; End:",c_d,"\n")