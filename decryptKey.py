import rsa
from cryptography.fernet import Fernet

def Decryption(role):
    try:
        private_key = open('private_key3.key', 'rb')
        prikey = private_key.read()
        prkey = rsa.PrivateKey.load_pkcs1(prikey)

        # Read the encrypted file
        encrypted_key = open("keyopen", "rb")
        ekey = encrypted_key.read()

        # Decrypt the data
        dkey = rsa.decrypt(ekey, prkey)

        cipher = Fernet(dkey)

        if role == 'Admin':
            encrypted_data = open("EncryptedFilesAdmin", "rb")
        elif role == 'User':
            encrypted_data = open("EncryptedFilesUser", "rb")
        else:
            return "Invalid role"

        edata = encrypted_data.read()
        decrypted_data = cipher.decrypt(edata)
        data = decrypted_data.decode()
        return data

    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"Decryption error: {str(e)}"

# Call the decryption function
#role = "Admin"  # or "User"
#result = Decryption(role)
#print(result)
