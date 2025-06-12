from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def pad(data):
    # PKCS7 padding
    pad_len = AES.block_size - len(data) % AES.block_size
    return data + bytes([pad_len] * pad_len)

def encrypt_file(file_data, key):
    """
    Encrypts the given file data using AES CBC mode with the provided key.
    Returns the IV prepended to the encrypted data.
    """
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(file_data)
    encrypted = cipher.encrypt(padded_data)
    return iv + encrypted  # prepend IV for use in decryption

def decrypt_file(encrypted_data, key):
    """
    Decrypts the given encrypted data using AES CBC mode with the provided key.
    Assumes the first block_size bytes are the IV.
    Returns the original file data after removing padding.
    """
    iv = encrypted_data[:AES.block_size]
    encrypted = encrypted_data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = cipher.decrypt(encrypted)
    pad_len = padded_data[-1]
    return padded_data[:-pad_len]
