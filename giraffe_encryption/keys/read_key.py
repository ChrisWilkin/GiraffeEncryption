import rsa
from typing import Tuple
from pathlib import Path

GIRAFFE_PATH = Path.home() / Path(".giraffe")


def get_existing_keys() -> Tuple[rsa.PublicKey, rsa.PrivateKey]:
    """Generates a new RSA Giraffe public-private key pair"""
    if not GIRAFFE_PATH.exists():
        raise FileNotFoundError("Was unable to locate the ~/.giraffe directory. Consider running `giraffe-keygen`!")
    assert GIRAFFE_PATH.is_dir(), "Tried to use ~/.giraffe as directory but found file!"

    return (_read_public_key(), _read_private_key())

    
def _read_public_key() -> rsa.PublicKey:
    with open("../.giraffe/pub_key.giraffe", 'rb') as file:
        file_bytes = file.read()
        key_len = file_bytes[0]
        n_bytes = file_bytes[1: key_len + 1]
        e_bytes = file_bytes[key_len + 1:]

        n = int.from_bytes(n_bytes)
        e = int.from_bytes(e_bytes)

        return rsa.PublicKey(n, e)


def _read_private_key() -> rsa.PrivateKey:
    with open("../.giraffe/.giraffe", 'rb') as file:
        file_bytes = file.read()
        n_len = file_bytes[0]
        e_len = file_bytes[1]
        d_len = file_bytes[2]
        p_len = file_bytes[3]

        n_bytes = file_bytes[4: n_len + 4]
        e_bytes = file_bytes[n_len + 4: n_len + e_len + 4]
        d_bytes = file_bytes[n_len + e_len + 4: n_len + e_len + d_len + 4]
        p_bytes = file_bytes[n_len + e_len + d_len + 4: n_len + e_len + d_len + p_len + 4]
        q_bytes = file_bytes[n_len + e_len + d_len + p_len + 4:]

        n = int.from_bytes(n_bytes)
        e = int.from_bytes(e_bytes)
        d = int.from_bytes(d_bytes)
        p = int.from_bytes(p_bytes)
        q = int.from_bytes(q_bytes)

        return rsa.PrivateKey(n,e,d,p,q)