import math


def my_atkin(limit):
    second_limit = int(limit * 10)
    sqrt_lim = int(second_limit ** 0.5)
    is_prime = [False] * (second_limit + 1)
    is_prime[2] = True
    is_prime[3] = True

    x2 = 0
    for i in range(1, sqrt_lim + 1):
        x2 += 2 * i - 1
        y2 = 0
        for j in range(1, sqrt_lim + 1):
            y2 += 2 * j - 1

            n = 4 * x2 + y2
            if n <= limit and (n % 12 == 1 or n % 12 == 5):
                is_prime[n] = not is_prime[n]

            n -= x2
            if n <= limit and n % 12 == 7:
                is_prime[n] = not is_prime[n]

            n -= 2 * y2
            if (i > j) and (n <= limit) and (n % 12 == 11):
                is_prime[n] = not is_prime[n]

    result = [2, 3, 5]
    for i in range(6, limit + 1):
        if (is_prime[i]) and (i % 3 != 0) and (i % 5 != 0):
            result.append(i)
    return result


def atkins(limit):
    primes = [False] * limit
    sqrt_limit = int(math.sqrt(limit))

    x_limit = int(math.sqrt((limit + 1) / 2))
    for x in range(1, x_limit):
        xx = x*x

        for y in range(1, sqrt_limit):
            yy = y*y

            n = 3*xx + yy
            if n <= limit and n % 12 == 7:
                primes[n] = not primes[n]

            n += xx
            if n <= limit and n % 12 in (1, 5):
                primes[n] = not primes[n]

            if x > y:
                n -= xx + 2*yy
                if n <= limit and n % 12 == 11:
                    primes[n] = not primes[n]

    for n in range(5, limit):
        if primes[n]:
            for k in range(n*n, limit, n*n):
                primes[k] = False

    return [2, 3] + filter(lambda x: primes[x], range(5, limit))
