from os import urandom
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

def get_parameters():
    backend = default_backend()
    params = dh.generate_parameters(generator=2, key_size=2048, backend=backend)
    return params

def get_keys(params):
    priv_key = params.generate_private_key()
    pub_key = priv_key.public_key()
    salt = None
    info = "~center handshake".encode()
    return priv_key, pub_key, salt, info

def derive_keys(peer_pub_key):
    params = get_parameters()
    priv_key, pub_key, salt, info = get_keys(params)
    shared_key = priv_key.exchange(peer_pub_key)
    derived_key = HKDF(algorithm=SHA256(), length=32, salt=salt, info=info, 
        backend=backend).derive(shared_key)
    return derived_key