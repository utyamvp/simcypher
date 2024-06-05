import os
from cryptography.fernet import Fernet

def generate_key():
    # Генерация и возвращение ключа шифрования
    return Fernet.generate_key()

def encrypt_text(text, key):
    # Шифрование текстового сообщения
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(text.encode())
    print(f"Encrypted text: {encrypted_data.decode()}\n")
    return encrypted_data

def decrypt_text(encrypted_data, key):
    # Дешифрование текстового сообщения
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    print(f"Decrypted text: {decrypted_data.decode()}\n")

def encrypt_file(file_path, key):
    # Шифрование файла
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(plaintext)
    encrypted_file_path = file_path + '.encrypted'
    with open(encrypted_file_path, 'wb') as f:
        f.write(encrypted_data)
    print(f"File content: {plaintext.decode(errors='ignore')}")  # Выводим содержимое файла
    print(f"Encrypted text: {encrypted_data.decode(errors='ignore')}\n")  # Зашифрованное содержимое файла
    return encrypted_data

def decrypt_file(file_path, key):
    # Дешифрование файла
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    print(f"Decrypted text: {decrypted_data.decode(errors='ignore')}\n")  # Дешифрованное содержимое файла
    return decrypted_data

def process_files_in_directory(directory_path, key, action):
    # Шифрование или дешифрование всех файлов в директории
    for dirpath, _, filenames in os.walk(directory_path):
        for filename in filenames:
            if action == "encrypt" and filename.endswith(".txt"):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'rb') as f:
                    plaintext = f.read()
                cipher_suite = Fernet(key)
                encrypted_data = cipher_suite.encrypt(plaintext)
                encrypted_file_path = file_path + '.encrypted'
                with open(encrypted_file_path, 'wb') as f:
                    f.write(encrypted_data)
                print(f"File content: {plaintext.decode(errors='ignore')}")  # Выводим содержимое файла
                print(f"Encrypted text: {encrypted_data.decode(errors='ignore')}\n")  # Зашифрованное содержимое файла
            elif action == "decrypt" and filename.endswith(".txt.encrypted"):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'rb') as f:
                    encrypted_data = f.read()
                cipher_suite = Fernet(key)
                decrypted_data = cipher_suite.decrypt(encrypted_data)
                decrypted_file_path = file_path[:-10]  # Убираем .encrypted из названия файла
                with open(decrypted_file_path, 'wb') as f:
                    f.write(decrypted_data)
                print(f"Decrypted text: {decrypted_data.decode(errors='ignore')}\n")  # Дешифрованное содержимое файла

def main():
    key = generate_key()
    while True:
        print("Choose an option:")
        print("1. Encrypt/Decrypt a text message")
        print("2. Encrypt/Decrypt a file")
        print("3. Encrypt/Decrypt files in a directory")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            text = input("Enter the text to encrypt: ")
            encrypted_text = encrypt_text(text, key)
            decrypt_text(encrypted_text, key)
        elif choice == '2':
            file_path = input("Enter the file path to encrypt/decrypt: ")
            encrypted_data = encrypt_file(file_path, key)
            decrypted_data = decrypt_file(file_path + '.encrypted', key)
            with open(file_path, 'wb') as f:
                f.write(decrypted_data)
        elif choice == '3':
            directory_path = input("Enter the directory path: ")
            process_files_in_directory(directory_path, key, action="encrypt")
            process_files_in_directory(directory_path, key, action="decrypt")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
