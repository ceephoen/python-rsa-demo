# -*- coding: utf-8 -*-
"""
encrypt/decrypt function
"""
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os


def gen_key():
    """generate key"""
    # key pair
    key = RSA.generate(2048)

    # private_key
    private_key = key.export_key()
    file_out = open(os.path.dirname(__file__)+os.path.sep+"private_key.pem", "wb")
    file_out.write(private_key)

    # public_key
    public_key = key.publickey().export_key()
    file_out = open(os.path.dirname(__file__)+os.path.sep+"public_key.pem", "wb")
    file_out.write(public_key)


def encrypt(s):
    """encrypt"""
    public_pem = open(os.path.dirname(__file__)+os.path.sep+"public_key.pem").read()
    public_key = RSA.import_key(public_pem)
    cipher_rsa = PKCS1_OAEP.new(public_key)

    encrypt_text = cipher_rsa.encrypt(s.encode('utf-8'))

    return encrypt_text


def decrypt(d):
    """decrypt"""
    private_path = open(os.path.dirname(__file__)+os.path.sep+"private_key.pem").read()
    private_key = RSA.import_key(private_path)

    cipher_rsa_decrypt = PKCS1_OAEP.new(private_key)
    decrypt_text = cipher_rsa_decrypt.decrypt(d)

    return decrypt_text
