import secrets
import socket
import ipaddress
import dhmath
import sys

#Default parameters taken from RFC 3526 (2048 bit Diffie Hellman Group with ID 14
default_p = int("FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF",16)
default_g = 2


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

#determine if the user wants to enter parameters (Alice) or accept (Bob) parameters from the other user
def get_alice():
  while True:
    answer = input("Pick Alice or Bob: ").lower()
    if (answer == "alice"):
      return True
    if (answer == "bob"):
      return False

#Let the user pick the size of the original secret key in bit
def get_key_size():
  while True:
    inp = input("Pick key size in bits (256 bit or more recommended): ")
    try:
      n = int(inp)
      if dhmath.checkkeysize(n):
        return n
    except Exception as e:
      print(e)
        
#Let the user enter a modulus p or use the default modulus
def get_modulus():
  while True:
    inp = input("Pick modulus (safe prime with at least 180 bit) or - highly recommended - use default by typing 'd': ")
    if inp == "d":  
      print("using default 2048 bit modulus.")
      return default_p    
    try:
      n = int(inp)
      if dhmath.checkmodulus(n):
        return n
    except Exception as e:
      print(e)

#Let the user enter a generator for the cylic group modulo p, or use the default
def get_generator(p):
  if p == default_p:
    return default_g
  while True:
    inp = input("Pick base (integer) or use default by typing 'd': ")
    if inp == "d":
      print("Using default base.")
      return  default_g
    try:
      n = int(inp)
      if dhmath.checkgenerator(n,p):
        return n
    except Exception as e:
      print(e)

#Let the user enter the partner's IP
def get_partner_ip():
  noIP = True
  print("Please enter your partner's IP address to start the key exchange. Use the format xxx.xxx.xxx.xxx.")
  while noIP:
    partnerIP = input("IP: ")
    try:
      IP = ipaddress.ip_address(partnerIP)
      noIP = False
      return partnerIP
    except Exception as e:
      print(e)

if __name__ == '__main__':

  print("Diffie Hellman Key Exchange")
  print("===========================")



  #print own IP
  print("Your IP address is: " + str(get_ip_address()))
  
  #determine role
  print("Do you want to act as Alice (setting the parameters and establishing the connection) or Bob (accepting your partner's parameters)?")
  alice = get_alice()
  
  initial = False
  
  if alice:
    #if this user is alice, ask the user for the partner's IP address
    IP = get_partner_ip()
    input("press any key when Bob is ready.")
    #create a connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((IP, 3457))
    #send initial "DH", expect "DH" as an answer
    str_send = "DH"
    s.send(bytes(str_send, "utf-8"))
    r = s.recv(1024).decode("utf-8")
    if (r == "DH"):
      print("Key exchange initiated.")
      initial = True

  else:      
    #if this user is bob, create a listening socket
    print("Ready to start.")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((get_ip_address(), 3457))
    s.listen(1)
    c, addr = s.accept()
    #wait for initial "DH" message and reply with "DH"
    str_recv, temp = c.recvfrom(1024)
    r = str_recv.decode("utf-8")
    if (r == "DH"):
      str_send = "DH"
      c.send(bytes(str_send, "utf-8"))
      initial = True
      print("Diffie Hellman Key Exchange started. Partner address: " + str(addr))
  
  
  #if initial exchange didn't work, exit program
  if not initial:
    print("Error: Something went wrong.")
    s.close()
    sys.exit()
  
  
  exchange_successful = False
  
  if alice:
    #If the user is Alice: determine the parameters 
    keysize = get_key_size()
    modulus = get_modulus()
    g = get_generator(modulus)    
    #put all the parameters in one string
    params = str(keysize)+"\n"+str(g)+"\n"+str(modulus)
    #and send it to the partner
    s.send(str(params).encode('utf8'))
    #the partner should answer with "OK" or "NO"
    r = s.recv(1024).decode("utf-8")
    if (r == "OK"):
      exchange_successful = True
      print("parameters successfully sent.")
    if (r == "NO"):
      print("Error: Parameters rejected.")
    
  else:
    #if the user is Bob: wait for Alice to send parameters
    r = c.recv(1024)
    params = r.decode("utf-8")
    #extract parameters from the received string
    parameters = params.split("\n")
    keysize = int(parameters[0])
    g = int(parameters[1])
    modulus = int(parameters[2])
    
    #check validity of parameters    
    key_ok = dhmath.checkkeysize(keysize)
    p_ok = False
    g_ok = False
    if modulus == default_p:
      p_ok = True
      if g == 2:
        g_ok = True
      else:
        print("Bad generator.")
    else:     
      p_ok = dhmath.checkmodulus(modulus)
      g_ok = dhmath.checkgenerator(g,modulus)
    #if parameters are not valid, send "NO", otherwise, send "OK" to Alice
    if not (p_ok and key_ok and g_ok):
      print("Parameters not okay.")
      c.send(bytes("NO", "utf-8"))
    else:
      print("Received paramters successfully.")
      exchange_successful = True
      c.send(bytes("OK", "utf-8"))
  
  #if something went wrong, exit the program
  if not exchange_successful:
    print("Parameter exchange not successful. Closing connection.")
    s.close()
    sys.exit()

  #both sides now compute their own private secret
  b = int(keysize / 8)    
  private = secrets.token_hex(b)
  print("Your private key is: " + private)
  private = int(private,16)
  #compute the shared secret to send over to the partner
  share = pow(g, private, modulus)
  print("Your shared secret is: " + format(share, 'x') + "\n")
  
  partnershare = 0
  if alice:
    #if the user is Alice, start with sending own shared secret
    print("Sending own shared secret.")
    s.send(bytes(format(share,"x"), "utf-8"))
    #then receive partner's shared secret
    partnershare = s.recv(1024).decode("utf-8")
    print("Received partner's shared secret " + partnershare + "\n")
  
  else:
    #if the user is Bob, wait for Alice's shared secret
    str_recv, temp = c.recvfrom(1024)
    partnershare = str_recv.decode("utf-8")
    print("Received partner's shared secret " + partnershare + "\n")
    #then send own shared secret to Alice
    print("Sending own shared secret.")
    c.send(bytes(format(share,"x"), "utf-8"))
  
  print("Exchange completed.\n")
  
  #both sides compute the common secret
  print("The common secret is: " + format(pow(int(partnershare,16), private, modulus), 'x'))
  
  
  s.close()

  #https://github.com/LauraWartschinski/zidryx/blob/
