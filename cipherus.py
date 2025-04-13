from cryptography.fernet import Fernet, InvalidToken
import os
import random
import string
import hashlib

marker = b"CipherusENC::"
key_signature = b"CipherusKEY::"

# Generate a secret key
def generate_key(filename):
    key = Fernet.generate_key()
    strid = generate_random_strid()
    with open(filename, "wb") as key_file:
        key_file.write(key_signature + strid.encode() + b"::" + key)

# Load secret key
def load_key(secret_key_file):
    with open(secret_key_file,"rb") as file:
        content = file.read()
        if not content.startswith(key_signature):
            raise ValueError("Incorrect key file format! This is not a cipherus key.")

        # Extract the strid (up to the "::" marker, which we added in generate_key)
        key_start = len(key_signature)
        strid_end = content.find(b"::", key_start)  # Find the position of "::"
        
        if strid_end == -1:
            raise ValueError("Invalid key format: strid not found.")

        # Extract strid and key
        strid = content[key_start:strid_end].decode() 
        key = content[strid_end + 2:] 

        return strid, key

# Random string of 4 to 8 letters
def generate_random_strid():
    length = random.randint(4, 8)
    return ''.join(random.choices(string.ascii_lowercase, k=length))

# Generate hash
def generate_hash(input_string):
    hash_obj = hashlib.sha256(input_string.encode())
    full_hash = hash_obj.hexdigest()

    input_length = len(input_string)
    min_length = 8  
    max_length = 64  
    
    hash_length = min(max(min_length, int(input_length * 2)), max_length)
    
    return full_hash[:hash_length]

# Check hash 
def check_hash(strid, encrypted_data):
    embedded_hash = encrypted_data[len(marker):len(marker) + len(generate_hash(strid))]
    current_hash = generate_hash(strid).encode()
    return embedded_hash == current_hash


# Encryption
def encrypt_file(filename, strid, key):

    try:
        with open(filename, "rb") as file:
            original = file.read()

        if original.startswith(marker):
            print("The file is already encrypted with cipherus!!")
            return
        
        fernet = Fernet(key)
        strid_hash = generate_hash(strid).encode()
        encrypted = marker + strid_hash + fernet.encrypt(original)  

        with open(filename, "wb") as encrypted_file:
            encrypted_file.write(encrypted)

        print(f"File {filename} successfully encrypted")
    except Exception as e:
        print(f"An unexpected error occurred during encryption: {e}")


# Decryption
def decrypt_file(filename, strid, key):

    try:
        with open(filename, "rb") as file:
            encrypted = file.read()

        if not encrypted.startswith(marker):
            print("The file is not encrypted with cipherus!!")
            return

        strid_hash = generate_hash(strid).encode()
        if not check_hash(strid, encrypted):
            print("Error: Hash mismatch — the key does not match this file or the file has been tampered with.")
            return
        
        encrypted = encrypted[len(marker) + len(strid_hash):] 
        fernet = Fernet(key)

        decrypted = fernet.decrypt(encrypted)

        with open(filename, "wb") as decrypted_file:
            decrypted_file.write(decrypted)

        print(f"File {filename} successfully decrypted")
    except InvalidToken:
        print("Error: Invalid key or file was not encrypted correctly. Decryption failed.")
    except Exception as e:
        print(f"An unexpected error occurred during decryption: {e}")


def main():
    while True:
        print("\nCipherus Menu:")
        print("1. Encryption")
        print("2. Decryption")
        print("3. Exit (Press 'ctrl + c' to quit)")

        try:
            choice = int(input("Option: "))
        except ValueError:
            print("Enter a valid number.")
            continue
        except KeyboardInterrupt:
            print("Exiting Cipherus.")
            break
        except Exception as e:
            print(f"Error: {e}")

# Choice 1
        if choice == 1:
            selected_file = input("Select a file to Encrypt: ")
            if not os.path.isfile(selected_file):
                print(f"Error: file {selected_file} not found")
                continue
            
            selected = False
            while not selected:
                create_key_permission = input("Create a new secret key? (default y) (y/n): ")
                create_key_permission = create_key_permission.lower()

                if create_key_permission in ["y", "yes", ""]:
                    secret_key_file = input("Enter a filename to store the cipher key (press Enter for default 'secret.cphkey'): ") 
                    if not secret_key_file:
                        secret_key_file = "secret.cphkey"
                        selected = True
                    elif not secret_key_file.endswith(".cphkey"):
                        secret_key_file += ".cphkey"
                        selected = True
                    else:
                        selected = True
                    generate_key(secret_key_file)

                elif create_key_permission in ["n", "no"]:
                    while True:
                        secret_key_file = input("Select the cipher key (must have '.cphkey' extension): ")

                        if not secret_key_file.endswith(".cphkey"):
                            print("Error: Wrong file, '.cphkey' extension not found")
                        elif not os.path.isfile(secret_key_file):
                            print(f"Error: file '{secret_key_file}' not found")
                        else:
                            selected = True
                            break
                    
                else:
                    print("Please enter a valid option")

            try:
                strid, key = load_key(secret_key_file)

                if key:
                    encrypt_file(selected_file, strid, key)
            except ValueError as ve:
                print(f"Error: {ve}")


# Choice 2
        elif choice == 2:
            selected_file = input("Select a file to Decrypt: ")
            if not os.path.isfile(selected_file):
                print(f"Error: file '{selected_file}' not found")
                continue

            while True:
                secret_key_file = input("Select the cipher key (must have '.cphkey' extension): ")
                if not secret_key_file.endswith(".cphkey"):
                    print("Error: Wrong file, '.cphkey' extension not found")
                elif not os.path.isfile(secret_key_file):
                    print(f"Error: file {secret_key_file} not found")
                else:
                    break

            try:
                strid, key = load_key(secret_key_file)

                if key:
                    decrypt_file(selected_file, strid, key)
            except ValueError as ve:
                print(f"Error: {ve}")

# Choice 3
        elif choice == 3:
            print("Exiting Cipherus.")
            break

        else:
            print("Invalid choice. Please select between 1-3.")


# Main Start
if __name__ == "__main__":
    main()