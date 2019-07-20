from math import gcd
from eratosfen import get_primes
from random import choices

def rsa(x, n, Px):
    res = Px
    for _ in range(1, x):
        res = (res * Px) % n
    return res

limit = 1000
hack_limit = limit

def encrypt(text, e, n):
    result = []
    for i in range(len(text)):
        if i == 0:
            x = 0
        else:
            x = ord(text[i-1])
        result.append(rsa(e, n, ord(text[i]) + x))
    return ''.join(map(chr, result))

def decrypt(text, d, n):
    result = []
    for i in range(len(text)):
        temp = rsa(d, n, ord(text[i]))
        if i == 0:
            result.append(temp)
        else:
            result.append(temp - result[-1])
    return ''.join(map(chr, result))
    


primes = get_primes(limit)

p, q = choices(primes[-int(limit * 0.1):], k=2)
n = p * q
f = (p - 1) * (q - 1)

e = 0
for i in primes:
    if gcd(i, f) == 1:
        e = i
        break

d = f + 1
while (d * e) % f != 1:
    d += 1



my_str = 'some text'
encrypted = encrypt(my_str, e, n)
# print(encrypted)
decrypted = decrypt(encrypted, d, n)
print(encrypted, decrypted)
