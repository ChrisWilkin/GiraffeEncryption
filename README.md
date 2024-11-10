             _______ _                ___    ___                  
            (_______|_)              / __)  / __)                 
            _   ___ _  ____ _____ _| |__ _| |__ _____            
            | | (_  | |/ ___|____ (_   __|_   __) ___ |           
            | |___) | | |   / ___ | | |    | |  | ____|           
            \_____/|_|_|   \_____| |_|    |_|  |_____)                                                            
         _______                                    _             
        (_______)                               _  (_)            
        _____   ____   ____  ____ _   _ ____ _| |_ _  ___  ____  
        |  ___) |  _ \ / ___)/ ___) | | |  _ (_   _) |/ _ \|  _ \ 
        | |_____| | | ( (___| |   | |_| | |_| || |_| | |_| | | | |
        |_______)_| |_|\____)_|    \__  |  __/  \__)_|\___/|_| |_|
                                (____/|_| Created by Chris Wilkin
               
                                                                  
Giraffe Encryption is a package for encrypting and decrypting secrets in a fun and quirky way. It makes use of RSA public-private key encryption.

## Terminal Commands

### giraffe-keygen
Generates a brand new set of RSA public and private keys in the `~/.giraffe` directory. Once a new set of keys has been created, the old keys are lost forever

### giraffe-printkey
Displays the `Public Key String` that can be copied and shared with others. This string is what enables other people to encrypt files and messages they want to send to you.

### giraffe-encrypt (-m -f file_path -o output_dir)
Encrypts either a file or a message (prompted for entry after running command) and saves the encrypted data as a file named `secret.giraffe` at the specified output directory.
Prior to encryption, a Public Key String needs to be entered. This should be provided by the person you want to send the file to.

When -f is used, the file at the provided path will be encrypted.
When -m is passed (just a flag), you will receive a prompt to type in the message you want to encrypt
When -o is not used, the encrypted file will be saved to the current working directory.

-m and -f cannot be used at the same time.

### giraffe-decrypt (-f file_path -o output_dir)
Decrypts the specified `.giraffe` file using your Private Key. If the decrypted file produces a file, that file will be saved at the specified output directory. Or if not output directory is provided, it will be saved in the same directory as the encrypted file.




