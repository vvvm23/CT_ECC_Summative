from vvvm23 import *
import random

nb_test_one = 10000
nb_test_two = 10000
nb_test_three = 10

# Test of full cycle with no bit changes #
r = m.floor(m.log2(nb_test_one)) + 1
for i in range(nb_test_one):
    c = decimalToVector(i, r)
    assert c == dataFromMessage(messageFromCodeword(hammingDecoder(hammingEncoder(message(c)))))

# Test of full cycle with one bit change #
r = m.floor(m.log2(nb_test_two)) + 1
for i in range(nb_test_two):
    c = decimalToVector(i, r)
    c_message = message(c)
    c_encode = hammingEncoder(c_message)

    j = random.randint(0, len(c_encode) - 1)

    c_encode[j] = (c_encode[j] + 1) % 2

    c_decode = hammingDecoder(c_encode)
    c_codeword = messageFromCodeword(c_decode)
    c_data = dataFromMessage(c_codeword)

    assert c_data == c

# Test of full cycle with two bit changes #
r = m.floor(m.log2(nb_test_three)) + 1
count = 0
correct = 0
for i in range(nb_test_three):
    c = decimalToVector(i, r)
    c_message = message(c)
    c_h = hammingEncoder(c_message)

    j = random.sample(range(len(c_h) - 1), 2)
    c_h[j[0]] = (c_h[j[0]] + 1) % 2
    c_h[j[1]] = (c_h[j[1]] + 1) % 2

    c_decode = hammingDecoder(c_h)
    c_codeword = messageFromCodeword(c_decode)
    c_data = dataFromMessage(c_codeword)

    count += 1
    if c_data == []:
        correct += 1

print("{0}/{1}".format(correct, count))
