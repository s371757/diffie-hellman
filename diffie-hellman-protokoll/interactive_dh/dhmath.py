#check if a number is a prime number
def is_prime(n):
    n = abs(int(n))
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    x = 3
    while (x**2 <= n):
        if n % x == 0:
            return False
        x = x+2
    return True

    
#check if a number n is a safe prime, d.h. if n = (2*q)+1 for another prime q
def is_safe_prime(n):
    q = ((n-1)//2)
    return is_prime(q)


#check if g is a generator for the cyclic group modulo p
def checkgenerator(g,p):
  print("Checking the generator. This might take a while.")
  if not is_safe_prime(p):
    print("The prime is not a safe prime.")
    return False
  #if p is a safe prime, then (2*q)-1 = p for a prime q
  #this means that p-1 only has the prime factors q and 2
  q = ((p-1)//2)
  #to check if g is a generator for the cyclic group of integers modulo p
  #we have to check if g ^ ((p-1)/f) is not congruent to 1 (modulo p)
  #for all prime factors f of p-1. The prime factors are q and 2.
  if pow(g,q,p) == 1 or pow(g,2,p) == 1:
    return False
  else:
    return True

#check if the key size is valid
def checkkeysize(n):
    if n < 160:
      print("Key size should be at least 160 bit.")
      return False
    elif n > 1024:
      print("Key size of more than 1024 seems a bit too much.")
      return False
    elif n % 8 != 0:
      print("key size should be a multiple of 8.")
      return False
    else:
      return True
  
#check if the prime modulus is valid
def checkmodulus(n):
  if n < 2:
    print("Not a positive prime number.")
    return False
  bitlength = len(bin(n))-2  
  if not is_prime(n):
    print(str(n) + " is not a prime number.")
    return False  
  if not is_safe_prime(n):
    print(str(n) + " is not a safe prime number.")
    return False
  if bitlength < 256:
    print("Warning. This number has " + str(bitlength) + " bit. It is recommended to use at least 256 bit or more.")
  return True
  

#https://github.com/LauraWartschinski/zidryx/blob/  
