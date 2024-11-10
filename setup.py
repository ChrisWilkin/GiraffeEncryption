from setuptools import setup, find_packages

setup(
    name="giraffe_encryption",
    version="0.1.2",
    packages=find_packages(),
    install_requres=[
        "rsa>=4.9",
        ""
    ],
    entry_points={
        "console_scripts": [
            "giraffe-keygen = giraffe_encryption.keys:giraffe_keygen",
            "giraffe-printkey = giraffe_encryption.keys:print_public_key",
            "giraffe-encrypt = giraffe_encryption.encryption.encrypt:encrypt_command",
            "giraffe-decrypt = giraffe_encryption.decryption.decrypt:decrypt_command"
        ]
    }
)