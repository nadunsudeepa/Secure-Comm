import rsa
from cryptography.fernet import Fernet

def KeyGeneration():
    #create symetric key
    key=Fernet.generate_key()

    #write a key
    k = open('message3.key','wb')
    k.write(key)
    k.close()

    #create private and public key
    (pubkey,privkey)=rsa.newkeys(2048)

    #write a public key
    public_key = open('public_key3.key','wb')
    public_key.write(pubkey.save_pkcs1('PEM'))
    public_key.close()

    #write a private key
    private_key = open('private_key3.key','wb')
    private_key.write(privkey.save_pkcs1('PEM'))
    private_key.close()

#KeyGeneration()