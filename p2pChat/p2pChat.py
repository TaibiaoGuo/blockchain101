# !/usr/bin python3
# encoding:utf-8
'''
 @Time     :2020/10/18 9:05 AM
 @Author   :TaibiaoGuo
 @FileName :p2pChat.py
 @Github   :https://github.com/TaibiaoGuo
 @Describe :
'''

import socketserver


class ServerFactory:
    """
    服务端的高层次抽象模型,定义了Server的基本接口模型
    抽象工厂模式，定义了服务器实现必须要实现的接口
    """

    def new_server(self, server_ip, server_port):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()

    def pong(self):
        raise NotImplementedError()


class ClientFactory:
    """
    客户端的高层次抽象模型，定义了客户端的基本接口模型
    抽象工厂模式，定义了客户端实现必须要实现的接口
    """

    def new_client(self, server_ip, server_port):
        raise NotImplementedError()

    def ping(self):
        raise NotImplementedError()

    def message_handle(self):
        raise NotImplementedError()


class P2PServer(ServerFactory, socketserver.TCPServer):
    """
    P2PServer 实现了P2P网络的服务端抽象工厂
    """

    def __init__(self):
        self.server_ip = None
        self.server_port = None
        self.sock = None
        socketserver.TCPServer.__init__(self, (self.server_ip, self.server_port))

    def new_server(self, server_ip='0.0.0.0', server_port=12467):
        '''
        创建一个TCP类型的socketserver
        '''

    def run(self):
        pass


class Peer:
    """
    Peer 定义了一个点对点网络的节点
    """

    def __init__(self):
        pass


class Bottle:
    def __init__(self):
        pass


class Chat:
    """
    Chat 定义了聊天
    """

    def __init__(self):
        pass


class Message:
    """
    Message 定义了消息
    """

    def __init__(self):
        pass


class Exchange:
    """
    实现一个简单的消息发布订阅模型用于客户端和服务端间的交互
    """

    def __init__(self):
        self._subscribers = set()

    def attach(self, channel):
        self._subscribers.add(channel)

    def detach(self, channel):
        self._subscribers.remove(channel)

    def send(self, msg):
        for subscriber in self._subscribers:
            subscriber.send(msg)


class TimeQueue:
    """
    TimeQueue 实现了一个带超时的队列，队列中的元素会在超时后自动删除。
    包括基队列time_queue_base、先进先出队列FIFO_time_queue、先进后出队列LIFO_time_queue。
    """


if __name__ == '__main__':
    # 设置服务端的地址
    address_server = ('0.0.0.0', 12467)
    # 设置客户端的地址，客户端只能在本机访问。
    address_client = ('127.0.0.1', 12468)
