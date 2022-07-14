import random
from typing import Tuple, List
from contracts import ic, natural

'''
@desc: Sieve of Eratosthenes
'''
@ic(n = natural)
def _eratosthenes(n: int) -> List[int]:
  primes, p = [1] * (n + 1), 2
  primes[0] = primes[1] = 0
  while(p * p <= n):
    if(primes[p]):
      for i in range(p * p, n + 1, p):
        primes[i] = 0
    p += 1
  
  c = 0
  for i in range(len(primes)):
    if(primes[i]):
      primes[c] = i
      c += 1
  
  return primes[:c]

'''
@desc: Select three random elements from a list of primes
'''
@ic(length = natural)
def _setup(length: int) -> Tuple[int, int, int]:
  sieve = _eratosthenes(length)
  return random.choice(sieve), \
         random.choice(sieve), \
         random.choice(sieve)

'''
@desc: Linear congruential
'''
@ic(seed = natural)
def lcg(seed: int, length: int) -> int:
  a, c, m = _setup(length)
  return ((a * seed) + c) % m