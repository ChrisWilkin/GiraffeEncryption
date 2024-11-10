import rsa
import os
from pathlib import Path
from .. import RSA_KEY_BITS
from .read_key import get_existing_keys

GIRAFFE_PATH = Path.home() / Path(".giraffe")


def print_public_key(file: Path = GIRAFFE_PATH):
    if not file.exists():
        os.makedirs(file)
    assert file.is_dir(), f"Tried to use {file} as directory but found file!"
    public_key, _ = get_existing_keys()
    print(f"START:{public_key.n}:{public_key.e}:END")


def giraffe_keygen():
    """Generates a new RSA Giraffe public-private key pair"""
    if not GIRAFFE_PATH.exists():
        os.makedirs(GIRAFFE_PATH)
    assert GIRAFFE_PATH.is_dir(), "Tried to use ~/.giraffe as directory but found file!"

    public_key, private_key = rsa.newkeys(RSA_KEY_BITS)
    _write_private_key(private_key)
    _write_public_key(public_key)


def _to_bytes(i: int, size=None) -> bytes:
    if size is None:
        return i.to_bytes((i.bit_length() + 7) // 8, 'big')
    else:
        return i.to_bytes(size, 'big')


def _write_private_key(key: rsa.PrivateKey):
    """Writes Private Key values to binary file"""
    key_n = _to_bytes(key.n)
    key_e = _to_bytes(key.e)
    key_d = _to_bytes(key.d)
    key_p = _to_bytes(key.p)
    key_q = _to_bytes(key.q)

    len_key_n = _to_bytes(len(key_n), 1)
    len_key_e = _to_bytes(len(key_e), 1)
    len_key_d = _to_bytes(len(key_d), 1)
    len_key_p = _to_bytes(len(key_p), 1)

    with open(GIRAFFE_PATH / "private_giraffe.bin", 'wb') as file:
        file.write(len_key_n)
        file.write(len_key_e)
        file.write(len_key_d)
        file.write(len_key_p)
        file.write(key_n)
        file.write(key_e)
        file.write(key_d)
        file.write(key_p)
        file.write(key_q)


def _write_public_key(key: rsa.PublicKey):
    """Writes Public Key values to binary file"""
    key_n = _to_bytes(key.n)
    key_e = _to_bytes(key.e)
    len_key_n = _to_bytes(len(key_n), 1)

    with open(GIRAFFE_PATH / "public_giraffe.bin", 'wb') as file:
        file.write(len_key_n)
        file.write(key_n),
        file.write(key_e)

if __name__ == "__main__":
    giraffe_keygen()
    print_public_key()
