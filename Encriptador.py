import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

def encriptar(data,llave):
    data = pad(data.encode(),16)
    cipher = AES.new(llave.encode('utf-8'), AES.MODE_ECB)
    return binascii.hexlify(cipher.encrypt(data))

def desencriptar(data,llave):
    data = binascii.unhexlify(data)
    cipher = AES.new(llave.encode('utf-8'),AES.MODE_ECB)
    return unpad(cipher.decrypt(data),16)
