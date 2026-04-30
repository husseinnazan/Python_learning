# this is my first code wrote in the same day i started learning python :)
#this is a password manager that generate and save passwords and usernames.
import random
import string
import json
import os
from cryptography.fernet import Fernet
 #note : this function generates the password if the user granted access to generate one instead of writing his own password
def generate_password(length=12):
    all_characters = string.ascii_letters + string.digits + string.punctuation
    new_password = ""
    for _ in range(length):
        new_password += random.choice(all_characters)
    return new_password

def main():
    print("=========================================")
    print(" Your Web Identities & Passwords Manager   ")
    print("=========================================")
    
    identity_file = "identities.json"
    key_file = "secret.key"

    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, "wb") as f:
            f.write(key)
    else:
        with open(key_file, "rb") as f:
            key = f.read()

    fernet = Fernet(key)

    if os.path.exists(identity_file):
        with open(identity_file, "r") as f:
            try:
                encrypted_data = json.load(f)
                if "data" in encrypted_data:
                    decrypted_json = fernet.decrypt(encrypted_data["data"].encode()).decode()
                    saved_identities = json.loads(decrypted_json)
                else:
                    saved_identities = encrypted_data
            except (json.JSONDecodeError, Exception):
                saved_identities = {}
    else:
        saved_identities = {}
    
    while True:
        print("\nOptions:")
        print("1. Generate a new identity")
        print("2. View saved identities")
        print("3. Exit")
        
        choice = input("Select an option (1, 2, or 3): ").strip()
        
        if choice == "1":
            website = input("Which identity is this password for? ").strip()
            if not website:
                print("website name cannot be empty.")
                continue
            username = input("Enter your username: ").strip()
            generateinquiry = input("do you want to generate a password ? : ")
            if generateinquiry == "yes" or generateinquiry == "y" or generateinquiry == "true":
                password = generate_password()
            else:
                password = input("Enter your password : ").strip()
            saved_identities[website] = {"username": username, "password": password}
            print(f"Success! Identity for {website} generated and saved.")
            
        elif choice == "2":
            print("\n--- Saved Identities ---")
            if not saved_identities:
                print("No identities saved yet.")
            else:
                for site, idt in saved_identities.items():
                    print(f"{site}: {idt["username"]} - {idt["password"]}")
            
        elif choice == "3":
            json_string = json.dumps(saved_identities)
            encrypted_data = fernet.encrypt(json_string.encode()).decode()
            with open(identity_file, "w") as f:
                json.dump({"data": encrypted_data}, f, indent=4)
            print("Exiting Password Manager. Stay secure!")
            break
            
        else:
            print("Invalid option. Please enter 1, 2, or 3.")

