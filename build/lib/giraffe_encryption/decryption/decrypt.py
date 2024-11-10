import rsa
from pathlib import Path
from typing import Tuple, List
from argparse import ArgumentParser

from ..keys.read_key import get_existing_keys
from .. import ENCRYPTED_CHUNK_SIZE, LOGO


def decrypt_command():
    parser = ArgumentParser()
    parser.add_argument("-f", "--filepath", type=str, required=True,
                        help="Path to file you want to decrypt.")
    parser.add_argument("-o", "--output_dir", type=str, default="", 
                        help="Path to save the decrypted file. Defaults to parent directory of decrypted file.")
    args = parser.parse_args()

    decrypter = GiraffeDecrypter(
        file_path=Path(args.filepath),
        output_dir=Path(args.output_dir) if args.output_dir != "" else None
    )
    decrypter.decrypt()


class GiraffeDecrypter():

    def __init__(self, file_path: Path, output_dir: Path = None):
        assert file_path.is_file(), "File path option -f must be a file!"
        assert file_path.suffix == ".giraffe", "File path option -f must be of type `.giraffe`!"
        if output_dir is not None:
            assert output_dir.is_dir(), "Output dir option -o must be valid directory!"

        self.file_path = file_path
        self.output_dir = output_dir if output_dir is not None else file_path.absolute().parent.absolute()

        _, self.private_key = get_existing_keys()

    def decrypt(self):
        crypto = self._read_file()
        chunked_crypto = [
            crypto[i:i+ENCRYPTED_CHUNK_SIZE] for i in range(
                0, 
                ENCRYPTED_CHUNK_SIZE * (len(crypto)//ENCRYPTED_CHUNK_SIZE), 
                ENCRYPTED_CHUNK_SIZE
            )
        ]
        message = self._decrypt_message(chunked_crypto)
        message, filename = self._interpret_message(message)

        if filename is None:
            print(LOGO)
            print("Decoded message: ", message.decode())
            exit()

        with open(self.output_dir / filename, 'wb') as file:
            file.write(message)
        print(LOGO)
        print(f"\n\tDecrypted file successfully saved to \n\t{(self.output_dir / filename).absolute()}\n")

    def _read_file(self) -> bytes:
        with open(self.file_path, 'rb') as file:
            msg = file.read()
        return msg
    
    def _decrypt_message(self, msg_chunks: List[bytes]) -> bytes:
        msg_chunks = [rsa.decrypt(chunk, self.private_key) for chunk in msg_chunks]
        return b''.join(msg_chunks)

    @staticmethod
    def _interpret_message(msg: bytes) -> Tuple[bytes, str]:
        filename_length = msg[0]
        if filename_length == 0:
            return (msg[1:], None)
        
        filename = msg[1:filename_length+1].decode()
        message = msg[filename_length+1:]

        return (message, filename)
