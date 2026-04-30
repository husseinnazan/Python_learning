import random
import string
import json
import os

def generate_password(length=12):
    all_characters = string.ascii_letters + string.digits + string.punctuation
    new_password = ""
    for _ in range(length):
        new_password += random.choice(all_characters)
    return new_password

def main():
    print("========================================")
    print("   Secure CLI Password Manager   ")
    print("========================================")
    
    identity_file = "identities.json"
    if os.path.exists(identity_file):
        with open(identity_file, "r") as f:
            try:
                saved_identities = json.load(f)
            except json.JSONDecodeError:
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
            with open(identity_file, "w") as f:
                json.dump(saved_identities, f, indent=4)
            print("Exiting Password Manager. Stay secure!")
            break
            
        else:
            print("Invalid option. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
