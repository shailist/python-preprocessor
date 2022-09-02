from encodings import utf_8
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad

KEY_SIZE = 16
BLOCK_SIZE = 16

def create_key(password):
    SALT = b'MAGIC SALT'
    password = utf_8.encode(password)[0]
    digest = SHA256.new(password + SALT).digest()
    key = digest[:KEY_SIZE]
    digest = SHA256.new(key + SALT).digest()
    iv = digest[:BLOCK_SIZE]
    return key, iv

def create_vault(data, password):
    key, iv = create_key(password)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(key + data, BLOCK_SIZE)
    ciphertext = cipher.encrypt(padded)
    return ciphertext

def try_open_vault(data, password):
    key, iv = create_key(password)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        plaintext = cipher.decrypt(data)
        unpadded = unpad(plaintext, BLOCK_SIZE)
        assert unpadded[:KEY_SIZE] == key
    except Exception:
        raise ValueError('Incorrect password')
    return unpadded[KEY_SIZE:]
