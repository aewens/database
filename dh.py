from os import urandom
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

backend = default_backend()
params = dh.generate_parameters(generator=2, key_size=2048, backend=backend)

priv_key = params.generate_private_key()
pub_key = priv_key.public_key()
salt = None
info = "~center handshake".encode()

peer_priv_key = params.generate_private_key()
peer_pub_key = peer_priv_key.public_key()
peer_salt = urandom(32)

shared_key = priv_key.exchange(peer_pub_key)
derived_key = HKDF(algorithm=SHA256(), length=32, salt=salt, info=info, 
    backend=backend).derive(shared_key)

peer_shared_key = peer_priv_key.exchange(pub_key)
peer_derived_key = HKDF(algorithm=SHA256(), length=32, salt=salt, 
    info=info, backend=backend).derive(peer_shared_key)