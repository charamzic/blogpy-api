# python content_manager.py encrypt --all
# python content_manager.py decrypt prvni-clanek.cs.md
# python content_manager.py encrypt prvni-clanek.cs.md

import os
import sys
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")
POSTS_DIR = "posts"

if not ENCRYPTION_KEY:
    print("FATAL: ENCRYPTION_KEY is not set in .env! Cannot proceed.")
    sys.exit(1)

try:
    crypto = Fernet(ENCRYPTION_KEY.encode('utf-8'))
except Exception as e:
    print(f"FATAL: Failed to initialize Fernet. Is the key valid? Error: {e}")
    sys.exit(1)


def is_encrypted(filepath: str) -> bool:
    """Pokusí se dešifrovat soubor. Pokud se to podaří, je zašifrovaný."""
    try:
        with open(filepath, "rb") as f:
            encrypted_data = f.read()
        crypto.decrypt(encrypted_data)
        return True
    except Exception:
        return False


def process_file(filepath: str, action: str):
    """Provede šifrování/dešifrování s kontrolou stavu."""
    
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return

    is_file_encrypted = is_encrypted(filepath)
    filename = os.path.basename(filepath)

    if action == 'decrypt':
        if not is_file_encrypted:
            print(f"-> SKIPPING {filename}: Already decrypted (Text).")
            return
        
        with open(filepath, "rb") as f:
            encrypted_data = f.read()
        decrypted_bytes = crypto.decrypt(encrypted_data)
        with open(filepath, "w", encoding='utf-8') as f:
            f.write(decrypted_bytes.decode('utf-8'))
        print(f"-> DECRYPTED {filename} and ready for editing.")

    elif action == 'encrypt':
        if is_file_encrypted:
            print(f"-> SKIPPING {filename}: Already encrypted (Binary).")
            return
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        encrypted_data = crypto.encrypt(content.encode('utf-8'))
        
        with open(filepath, "wb") as f:
            f.write(encrypted_data)
        print(f"-> ENCRYPTED {filename}. Ready for commit.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python content_manager.py [command] [optional_filename]")
        print("\nCommands:")
        print("  decrypt [filename.md] - Decrypts one file for editing.")
        print("  encrypt [filename.md] - Encrypts one file after editing.")
        print("  encrypt --all         - Encrypts all currently decrypted files (SAFE).")
        print("  decrypt --all         - Decrypts all files (USE WITH CAUTION).")
        sys.exit(0)

    command = sys.argv[1]
    
    if command in ['decrypt', 'encrypt']:
        files_to_process = []
        
        if len(sys.argv) == 3 and sys.argv[2] == '--all':
            if command == 'decrypt':
                confirm = input(f"Are you sure you want to {command.upper()} ALL files in 'posts/'? (yes/no): ")
            else:
                confirm = 'yes'
            
            if confirm.lower() == 'yes':
                files_to_process = [os.path.join(POSTS_DIR, f) 
                                    for f in os.listdir(POSTS_DIR) 
                                    if f.endswith(".md")]
            else:
                print("Aborted.")
                sys.exit(0)
                
        elif len(sys.argv) == 3:
            filename = sys.argv[2]
            if not filename.endswith(".md"): filename += ".md"
            files_to_process.append(os.path.join(POSTS_DIR, filename))
            
        else:
            print(f"Missing filename or --all argument for command '{command}'.")
            sys.exit(1)

        for filepath in files_to_process:
            process_file(filepath, command)

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
