from os import urandom
from hmac import new as HMAC
from hashlib import sha256
from base64 import urlsafe_b64encode as ub64e, urlsafe_b64decode as ub64d
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt(message, key=None, nonce=None):
    if key is None:
        key = AESGCM.generate_key(bit_length=256)
    if nonce is None:
        nonce = urandom(12)
    data = message.encode()
    mac = HMAC(key, data + nonce, digestmod=sha256).digest()
    aesgcm = AESGCM(key)
    encrypted = aesgcm.encrypt(nonce, data, mac)
    splitter = "%%%".encode()
    return key, splitter.join([nonce, encrypted, mac])

def decrypt(key, source):
    splitter = "%%%".encode()
    nonce, encrypted, mac = source.split(splitter)
    aesgcm = AESGCM(key)
    data = aesgcm.decrypt(nonce, encrypted, mac)
    verify = HMAC(key, data + nonce, digestmod=sha256).digest()
    if mac != verify:
        return None
    return data.decode()