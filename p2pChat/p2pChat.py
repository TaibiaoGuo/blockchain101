from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as Sign_Pkcs
from Crypto.Cipher import PKCS1_v1_5 as Cipher_Pkcs
from Crypto import Util as Util_Crypto
from Crypto.Hash import SHA256
import base64
from .rsa import CryptoUtil


class Chat:
    def __init__(self):
        pass


class Bottle:
    def __init__(self):
        pass


class Id:
    _instance = None

    # __new__ 以单例模式保证了Id是全局唯一的
    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self._key = RSA.generate(2048)
        self.private_key = self._key.export_key()
        self.public_key = self._key.publickey()
        self.Id = self.public_key

    def get_id(self):
        return self.Id

    def digest(self, data):
        """
        使用摘要算法SHA256生成数据指纹，验证时也必须用SHA256
        :param data:
        :return:
        """
        return SHA256.new(data.encode('utf-8'))

    # def message_sign(self, data):
    #     """
    #     定义签名函数，能够使用指定的私钥对数据进行签名，返回签名结果
    #     :param data:
    #     :return:
    #     """
    #     # 获取消息的HASH值
    #     digest = self.digest(data)
    #     # 使用私钥对HASH值进行签名
    #     signature = Sign_Pkcs.new(self._key).sign(digest)
    #     # 将签名结果写入文件
    #     return signature
    def message_sign(self,data):
        digest = CryptoUtil.digest(data)
        signature = CryptoUtil.sign_by_private_key(self.private_key,digest)
        return signature

    def valid_message(self, data, signature):
        """
        定义签名验证函数，能够使用公钥对签名进行验证，返回验证结果
        :param data:
        :param signature:
        :return: True or False
        """
        digest = self.digest(data)
        try:
            #
            Sign_Pkcs.new(self.public_key).verify(digest, signature)
        except:
            return False
        else:
            return True




class Message(Id):
    def __init__(self, content, receiver):
        super(Message, self).__init__()
        self.content = content
        self.fromId = self.public_key
        self.toId = receiver
        # message_signature 使用fromId对应的证书进行了数字签名
        self.message_signature = self.message_sign(content)


class Route:
    def __init__(self):
        self.onlineUserNumber = 0

    def gossip_online_user_count(self):
        """
        gossip_online_user_count 基于gossip消息广播机制对全网在线用户数量进行维护。
        注意的是，各个节点的 onlineUserNumber 会存在差异，因为此方法不对各个节点的 onlineUserNumber 一致性做保证。
        """
        pass

