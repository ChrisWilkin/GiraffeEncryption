import typer
from encrypt import encryption
from decrypt import decryption

app = typer.Typer()


@app.command()
def encrypt(folder: str):
    encryption(folder)

@app.command()
def decrypt(folder: str):
    decryption(folder)

if __name__ == "__main__":
    app()