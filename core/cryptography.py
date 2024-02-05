from hashlib import sha256
import sys

def hash_password(password):
    return sha256(password.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    print(hash_password(" ".join(sys.argv[1:])))