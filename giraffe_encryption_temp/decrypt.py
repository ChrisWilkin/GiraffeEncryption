"""Main file for decrypting a GIRAFFE into a string"""
from typing import List
import numpy as np
import time
from pathlib import Path
import hashlib 
from getpass import getpass
from argparse import ArgumentParser

from .utils import describe_whitespace
from .ascii import giraffe


def decryption(folder: str = "."):
    try:
        load_dir = Path(folder)
        assert load_dir.is_dir(), "Load Directory must be a valid directory!"
    except:
        raise Exception(f"Passed load_dir {folder} could not be interpretted as a valid Path!")
    default_giraffe = giraffe
    print(
"""

                            /---------------------------------------\\
                            |                    ._ o o             |
                            |                   \_`-)|_             |
                            |           \\\\   ,""       \   //       |
                            |         \\\\   ,"  ## |   ^ ^.   //     |
                            |            ," ##   ,-\__    `.        |
                            |          ,"       /     `--.__)       |
                            |        ,"     ## /                    |
                            |      ,"   ##    /                     |
                            \\---------------------------------------/
        Welcome to GIRAFFEncryption - Please follow the steps below to retrieve your secret!
"""
    )
    time.sleep(1)
    print("\tFirst we need the name of your Giraffe...")
    giraffe_name = input("\n\t\tName: ").capitalize()

    try:
        with open(load_dir/f"{giraffe_name}.txt") as file:
            encrypted_giraffe = file.readlines()
    except:
        print(f"\n\tUnfortunately we weren't able to find {giraffe_name}. \n\tPlease check you have the correct name!")
        exit()

    print(f"\n\tBrilliant! Now we need the secret passphrase to reveal your secret!")
    passphrase = getpass("\n\t\tSecret passphrase: ")
    print(f"\n\tOkay... passing that information onto {giraffe_name}")

    secret = _decrypt(encrypted_giraffe, default_giraffe, passphrase)

    time.sleep(2)
    print(f"\n\n\t{giraffe_name} has responded!")
    print("\n\tHere is what he said:")
    time.sleep(1)
    print(f"\n\n\t\t\t*----   {secret}   ----*\n\n")
    

def _decrypt(encrypted_giraffe: List[str], default_giraffe: List[str], passphrase: str) -> str:
    hsh = int(hashlib.sha256(passphrase.encode('utf-8')).hexdigest(), 16) % 200
    password = ""
    for i in range(len(default_giraffe)):
        row = (hsh + i) % len(default_giraffe)
        if len(encrypted_giraffe[row]) == 121:
            break
        line = default_giraffe[row]
        struct = describe_whitespace(line)
        max_pos = sum(struct[1::2])
        char_pos = ((i + 1) * (hsh + i)) % max_pos
        char_segments = np.cumsum(struct[1::2])
        segment = min(np.where(char_segments > char_pos)[0] * 2 + 1)
        char_pos += sum(struct[0:segment:2])
        password += encrypted_giraffe[row][char_pos]

    return password


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        '--load_dir',
        type=str,
        help="Path to a directory for loading your giraffe file. Uses current directory if not set.",
        default="."
    )

    args = parser.parse_args()
    decryption(folder=args.load_dir)