from getpass import getpass
import rsa
from pathlib import Path
from typing import Tuple, List
from argparse import ArgumentParser

from ..keys.read_key import get_public_key_string
from .. import MESSAGE_CHUNK_SIZE, LOGO

def encrypt_command():
    parser = ArgumentParser()
    parser.add_argument("-f", "--filepath", type=str, default="", 
                        help="Path to file you want to encrypt. Cannot be used with -m")
    parser.add_argument("-o", "--output_dir", type=str, default=".", 
                        help="Directory to save the encrypted file.")
    parser.add_argument("-m", "--message", action='store_true',
                        help="Flag to indicate a message will be provided for encryption. Cannot be used with -f")
    args = parser.parse_args()

    encrypter = GiraffeEncrypter(
        file_path=Path(args.filepath) if args.filepath != "" else None,
        msg_flag=args.message,
        output_dir=Path(args.output_dir)
    )
    encrypter.encrypt()


class GiraffeEncrypter():

    def __init__(self, file_path: Path = None, msg_flag: bool = False, 
                 output_dir: Path = Path(".")):
        assert (file_path is None) == msg_flag, \
            "One of -f (--file-path) or -m (--message) must always be passed! Both cannot be used at the same time!"
        assert output_dir.is_dir(), \
            f"Save path option -o (--output-dir) is not a valid directory. Got {output_dir.absolute()}"
        if file_path is not None:
            assert file_path.is_file(), \
                "Provided file_path option -f (--file-path) is not a valid File!"

        self.file_path = file_path
        self.msg_flag = msg_flag
        self.output_dir = output_dir

        self.public_key = get_public_key_string()

    def encrypt(self):
        msg = self._apply_grff_format()
        encrypted_message = self._encrypt_message(msg)
        self._save_grff_file(encrypted_message)

    def _apply_grff_format(self) -> Tuple[str, bytes]:
        if self.msg_flag:
            msg = getpass("Enter secret: ").encode()
            filename = None
        else:
            with open(self.file_path, 'rb') as file:
                msg = file.read()
            filename = self.file_path.name
        
        byte_fn = filename.encode() if filename is not None else b''
        byte_fn_size = bytes([len(byte_fn)])

        if byte_fn == b'': # for messages
            return b''.join([byte_fn_size, msg])
        
        # for files
        return b''.join([byte_fn_size, byte_fn, msg])
    
    @staticmethod
    def _chunk_message(msg: bytes) -> List[bytes]:
        return [msg[i*MESSAGE_CHUNK_SIZE: (i+1)*MESSAGE_CHUNK_SIZE] 
                    for i in range(len(msg)//MESSAGE_CHUNK_SIZE + 1)]

    def _encrypt_message(self, msg: bytes) -> bytes:
        """Receives string message, returns encrypted message as bytes"""
        chunks = self._chunk_message(msg)
        chunks = [rsa.encrypt(chunk, self.public_key) for chunk in chunks]
        return b"".join(chunks)

    def _save_grff_file(self, encrypted_msg: bytes) -> None:
        """Writes the encrypted file in the directory"""
        with open(self.output_dir / "secret.giraffe", 'wb') as file:
            file.write(encrypted_msg)

        print(LOGO)
        print(f"\n\tEncrypted file saved successfully at \n\t{(self.output_dir / 'secret.giraffe').absolute()}\n")
