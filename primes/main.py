import time

from atkin import atkins, my_atkin
from eratosfen import eratosfen, boost_eratosfen

limit = 10000000

# # Atkin
# start_time = time.time()
# atkins_primes = my_atkin(limit)
# end_time = time.time()
# print(f"Atkin: limit = {limit}, time: {end_time - start_time}")

# Eratosfen
start_time = time.time()
eratosfens_primes = eratosfen(limit)
end_time = time.time()
print(f"Eratosfen: limit = {limit}, time: {end_time - start_time}")

# Eratosfen Boosted
start_time = time.time()
eratosfens_boost_primes = boost_eratosfen(limit)
end_time = time.time()
print(f"Eratosfen boosted: limit = {limit}, time: {end_time - start_time}")

# print(eratosfens_primes)
# print(eratosfens_boost_primes)

print(eratosfens_primes == eratosfens_boost_primes)
