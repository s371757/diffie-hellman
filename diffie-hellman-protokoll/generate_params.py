from sympy import isprime
import random

def find_sophie_germain_prime(limit=100000):
    """Find a random Sophie Germain prime less than the specified limit."""
    while True:
        q = random.randint(2, limit)
        if isprime(q) and isprime(2 * q + 1):
            return q

def find_generator(p):
    """Find a generator of the multiplicative group of integers modulo p."""
    factors = [f for f in prime_factors(p - 1)]
    for g in range(2, p - 1):
        if all(pow(g, (p - 1) // f, p) != 1 for f in factors):
            return g
    return None

def prime_factors(n):
    """Generate all prime factors of a given number n."""
    i = 2
    factors = set()
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.add(i)
    if n > 1:
        factors.add(n)
    return factors

# Find a random Sophie Germain prime
q = find_sophie_germain_prime()
p = 2 * q + 1

# Find a generator for Z_p*
generator = find_generator(p)

q, p, generator

