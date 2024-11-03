from setuptools import setup, find_packages

setup(
    name="giraffe_encryption",
    version="0.0.2",
    packages=find_packages(),
    install_requres=[],
    entry_points={
        "console_scripts": [
            "giraffe-encrypt = giraffe_encryption:encryption",
            "giraffe-decrypt = giraffe_encryption:decryption"
        ]
    }
)