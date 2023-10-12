import rsa
import base64
from cryptography.fernet import Fernet

def Encryption(message,role):

    #open the message key
    skey=open('message3.key','rb')
    key=skey.read()
    
    #create cliper
    cipher=Fernet(key)
    

    #encrypte the data
    encrypted_data=cipher.encrypt(bytes(message,'utf-8'))
    #edata = open("EncryptedFiles","wb")
    #edata.write(encrypted_data)

    public_key = open('public_key3.key','rb')
    pubkey = public_key.read()

    #encrypt the data
    pukey=rsa.PublicKey.load_pkcs1(pubkey)
    encrypted_key = rsa.encrypt(key,pukey)

    #sava the encrypt data to a file
    if role == 'Admin':
        #write encrypt_data
        edata = open("EncryptedFilesAdmin","wb")
        edata.write(encrypted_data)

    elif role == 'User':
        #write encrypt_data
        edata = open("EncryptedFilesUser","wb")
        edata.write(encrypted_data)

    edata=open("keyopen","wb")
    edata.write(encrypted_key)
#display message    
#message = input("Please enter the message: ")  
#role = input("enter the ser type: ")
#Encryption(message,role)