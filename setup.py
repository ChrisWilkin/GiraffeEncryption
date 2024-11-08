from setuptools import setup, find_packages

setup(
    name="giraffe_encryption",
    version="0.0.2",
    packages=find_packages(),
    install_requres=[
        "rsa"
    ],
    entry_points={
        "console_scripts": [
            "giraffe-keygen = giraffe_encryption:keys:giraffe_keygen",
            "giraffe-encrypt = giraffe_encryption:encryption:encrypt",
            "giraffe-decrypt = giraffe_encryption:decryption:decrypt"
        ]
    }
)