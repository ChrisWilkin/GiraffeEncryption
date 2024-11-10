import rsa
from typing import Tuple
from pathlib import Path
import math

GIRAFFE_PATH = Path.home() / Path(".giraffe")


def get_existing_keys() -> Tuple[rsa.PublicKey, rsa.PrivateKey]:
    """Generates a new RSA Giraffe public-private key pair"""
    if not GIRAFFE_PATH.exists():
        raise FileNotFoundError("Was unable to locate the ~/.giraffe directory. Consider running `giraffe-keygen`!")
    assert GIRAFFE_PATH.is_dir(), "Tried to use ~/.giraffe as directory but found file!"

    return (_read_public_key(), _read_private_key())


def get_public_key_string() -> rsa.PublicKey:
    """Requests Public Key string to be entered and returns actual PublicKey"""
    public_key_string = input("Enter Public Key string: ")
    return _parse_public_key_string(public_key_string)


def encrypted_message_chunks_size(n: int) -> int:
    """Returns the number of bytes in each encrypted message chunk"""
    return int(math.ceil(math.log(n, 2)) / 8)


def _parse_public_key_string(public_key_string: str) -> rsa.PublicKey:
    """Parses public key string into PublicKey class"""
    assert "START:" in public_key_string, "Key string does not contain START token!"
    assert ":END" in public_key_string, "Key string does not contain END token!"

    public_key_string = public_key_string.replace("START:", "")
    public_key_string = public_key_string.replace(":END", "")
    public_key_string = public_key_string.split(":")
    assert len(public_key_string) == 2, "Key string is not formatted correctly! Should be of the form \n\t" \
        "START:<key-value-1>:<key-value-2>:END"
    return rsa.PublicKey(int(public_key_string[0]), int(public_key_string[1]))

    
def _read_public_key() -> rsa.PublicKey:
    with open(GIRAFFE_PATH / "public_giraffe.bin", 'rb') as file:
        file_bytes = file.read()
        key_len = file_bytes[0]
        n_bytes = file_bytes[1: key_len + 1]
        e_bytes = file_bytes[key_len + 1:]

        n = int.from_bytes(n_bytes)
        e = int.from_bytes(e_bytes)

        return rsa.PublicKey(n, e)


def _read_private_key() -> rsa.PrivateKey:
    with open(GIRAFFE_PATH / "private_giraffe.bin", 'rb') as file:
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