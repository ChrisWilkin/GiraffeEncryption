"""Main file for encrypting a string into GIRAFFE"""
from typing import List
import numpy as np
from getpass import getpass
import time
from pathlib import Path
import hashlib

from utils import string_sub, get_giraffe, describe_whitespace

HAPPY_GERALD = r"""
               ._ o o 
               \_`-)|_
       \\   ,""       \   //
     \\   ,"  ## |   ^ ^.   //
        ," ##   ,-\__    `.
      ,"       /     `--.__)
    ,"     ## /      
  ,"   ##    /
"""

def encryption(folder: str):
    try:
        save_path = Path(folder)
        assert save_path.is_dir(), "Save Directory must be a valid directory!"
    except:
        raise Exception(f"Passed save_path {folder} could not be interpretted as a valid Path!")
    giraffe = get_giraffe()

    print("""

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
        Welcome to GIRAFFEncryption - Please follow the steps below to get your Giraffe!
""")
    time.sleep(1)
    print("\tFirst, let's name your Giraffe!")
    giraffe_name = input("\n\t\tName: ").capitalize()
    print(f"\n\t{giraffe_name}? That's a great name!")
    time.sleep(1)
    print("\n\tNow lets tell him your secret. I promise he won't tell anyone! (max 75 characters)")
    secret = getpass("\n\t\tYour super special secret: ")
    print(f"\n\tFinally, give {giraffe_name} a secret passphrase that only people allowed to hear the secret will know")
    print(f"\n\t***You'll need to remember this if you want your Giraffe to reveal the secret again!***")

    while True:
        password1 = getpass("\n\t\tPassphrase: ")
        password2 = getpass("\n\t\tRepeate Passphrase: ")
        if password1 != password2:
            print("\t\tPassphrases do not match! Try again!")
        else:
            print("\n\tPerfect, don't forget it!")
            break

    time.sleep(1)
    encrypted_giraffe = _encrypt(giraffe, secret, password1)
    with open(save_path/f"{giraffe_name}.txt", 'w') as file:
        file.writelines(encrypted_giraffe)

    print(f"\n\t{giraffe_name} has memorised your secret, and is waiting for you in {folder}!\n")

def _encrypt(giraffe: List[str], secret: str, passphrase: str) -> List[str]:
    hsh = int(hashlib.sha256(passphrase.encode('utf-8')).hexdigest(), 16) % 200
    secret = [p for p in secret]
    for i, char in enumerate(secret):
        row = (hsh + i) % len(giraffe)
        line = giraffe[row]
        struct = describe_whitespace(line)
        max_pos = sum(struct[1::2])
        char_pos = ((i + 1) * (hsh + i)) % max_pos
        char_segments = np.cumsum(struct[1::2])
        segment = min(np.where(char_segments > char_pos)[0] * 2 + 1)
        char_pos += sum(struct[0:segment:2])
        giraffe[row] = string_sub(line, char_pos, char)

    return giraffe