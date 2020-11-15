from Crypto.Hash import SHA256, HMAC
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad, pad
# from typing import bytes

"""
From
https://github.com/its-a-feature/Mythic/blob/master/mythic-docker/app/crypto.py#L91
"""


def aes256_decrypt(data: bytes, key: bytes):
    mac = data[-32:]
    iv = data[:16]
    message = data[16:-32]
    h = HMAC.new(key=key, msg=iv + message, digestmod=SHA256)
    h.verify(mac)
    decryption_cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_message = decryption_cipher.decrypt(message)
    return unpad(decrypted_message, 16)


def aes256_encrypt(data: bytes, key: bytes):
    h = HMAC.new(key, digestmod=SHA256)
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    ciphertext = cipher.encrypt(pad(data, 16))
    h.update(iv + ciphertext)
    return iv + ciphertext + h.digest()
