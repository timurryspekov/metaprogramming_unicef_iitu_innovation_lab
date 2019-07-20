
def get_primes(n):
    numbers = [7]
    is_prime = [False] * (n + 1)
    is_prime[2], is_prime[3], is_prime[5], is_prime[7] = True, True, True, True


    counter = 1
    counter_5 = 1
    for i in range(11, n, 2):
        if counter_5 == 5 or i == 15:
            counter_5 = 1
            continue
        if counter == 13:
            counter = 1
        if not (counter == 5 or counter == 7 or counter == 10 or counter == 12):
            is_prime[i] = True
            numbers.append(i)

        counter += 1
        counter_5 += 1

    i = 0
    limit_sqrt = n ** 0.5
    while numbers[i] <= limit_sqrt:
        if is_prime[numbers[i]]:
            for j in range(i, len(numbers)):
                if numbers[j] * numbers[i] > n:
                    break
                is_prime[numbers[j] * numbers[i]] = False
        i += 1

    result = [i for i in range(len(is_prime)) if is_prime[i]]
    return result

