# -*- coding: UTF-8 -*-
# ! /usr/bin/env python
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

import Crypto.Util


# 使用 rsa库进行RSA签名和加解密
class CryptoUtil:

    def get_max_length(self, rsa_key, encrypt=True):
        """加密内容过长时 需要分段加密 换算每一段的长度.
            :param rsa_key: 钥匙.
            :param encrypt: 是否是加密.
        """
        blocksize = Crypto.Util.number.size(rsa_key.n) / 8
        reserve_size = 11  # 预留位为11
        if not encrypt:  # 解密时不需要考虑预留位
            reserve_size = 0
        maxlength = blocksize - reserve_size
        return maxlength

    def encrypt_by_public_key(self, public_key, encrypt_message):
        """使用公钥加密.
            :param public_key:
            :param encrypt_message: 需要加密的内容.
            加密之后需要对接过进行base64转码
        """
        encrypt_result = b''
        max_length = int(self.get_max_length(public_key))
        cipher = Cipher_PKCS.new(public_key)
        while encrypt_message:
            input_data = encrypt_message[:max_length]
            encrypt_message = encrypt_message[max_length:]
            out_data = cipher.encrypt(input_data.encode(encoding='utf-8'))
            encrypt_result += out_data
        encrypt_result = base64.b64encode(encrypt_result)
        return encrypt_result

    def encrypt_by_private_key(self, private_key, encrypt_message):
        """使用私钥加密.
            :param private_key:
            :param encrypt_message: 需要加密的内容.
            加密之后需要对接过进行base64转码
        """
        encrypt_result = b""
        max_length = int(self.get_max_length(private_key))
        cipher = Cipher_PKCS.new(private_key)
        while encrypt_message:
            input_data = encrypt_message[:max_length]
            encrypt_message = encrypt_message[max_length:]
            out_data = cipher.encrypt(input_data.encode(encoding='utf-8').strip() + b"\n")
            encrypt_result += out_data
        encrypt_result = base64.b64encode(encrypt_result)
        return encrypt_result

    def decrypt_by_public_key(self, public_key, decrypt_message):
        """使用公钥解密.
            :param public_key:
            :param decrypt_message: 需要解密的内容.
            解密之后的内容直接是字符串，不需要在进行转义
        """
        decrypt_result = b""
        max_length = self.get_max_length(public_key, False)
        decrypt_message = base64.b64decode(decrypt_message)
        cipher = Cipher_PKCS.new(public_key)
        while decrypt_message:
            input_data = decrypt_message[:max_length]
            decrypt_message = decrypt_message[max_length:]
            out_data = cipher.decrypt(input_data.encode(encoding='utf-8'), '')
            decrypt_result += out_data
        return decrypt_result

    def decrypt_by_private_key(self, private_key, decrypt_message):
        """使用私钥解密.
            :param private_key:
            :param decrypt_message: 需要解密的内容.
            解密之后的内容直接是字符串，不需要在进行转义
        """
        decrypt_result = b""
        max_length = int(self.get_max_length(private_key, False))
        decrypt_message = base64.b64decode(decrypt_message)
        cipher = Cipher_PKCS.new(private_key)
        while decrypt_message:
            input_data = decrypt_message[:max_length]
            decrypt_message = decrypt_message[max_length:]
            out_data = cipher.decrypt(input_data, '')
            decrypt_result += str(out_data).encode(encoding='utf-8').strip() + b"\n"
        return decrypt_result

    def sign_by_private_key(self, private_key, message):
        """私钥签名.
            :param private_key:
            :param message: 需要签名的内容.
            签名之后，需要转义后输出
        """
        cipher = PKCS1_v1_5.new(private_key)  # 用公钥签名，会报错 raise TypeError("No private key") 如下
        # if not self.has_private():
        #   raise TypeError("No private key")
        hs = SHA256.new(message)
        signature = cipher.sign(hs)
        return base64.b64encode(signature)

    def verify_by_public_key(self, public_key, message, signature):
        """公钥验签.
            :param public_key:
            :param message: 验签的内容.
            :param signature: 对验签内容签名的值（签名之后，会进行b64encode转码，所以验签前也需转码）.
        """
        signature = base64.b64decode(signature)
        cipher = PKCS1_v1_5.new(public_key)
        hs = SHA256.new(message)

        # digest = hashlib.sha1(message).digest()  # 内容摘要的生成方法有很多种，只要签名和解签用的是一样的就可以

        return cipher.verify(hs, signature)

    def digest(self, data):
        """
        使用摘要算法SHA256生成数据指纹，验证时也必须用SHA256
        :param data:
        :return:
        """
        return SHA256.new(data.encode('utf-8'))