# !/usr/bin python3
# encoding:utf-8
'''
 @Time     :2020/10/18 9:05 AM
 @Author   :TaibiaoGuo
 @FileName :p2pChat.py
 @Github   :https://github.com/TaibiaoGuo
 @Describe :
'''


class Server:
    """
    服务端的高层次抽象模型,定义了Server的基本接口模型
    """

    def __init__(self):
        pass

    def new_server(self, ip, port):
        pass

    def pong(self):
        pass

    def handler_register(self,func,args,*,callback):
        return callback(func(*args))


class Client:
    """
    客户端的高层次抽象模型，定义了客户端的基本接口模型
    """

    def __init__(self):
        pass

    def new_client(self, ip, port):
        pass

    def ping(self):
        pass


class CLI(Client):
    """
    CLI格式的Client
    """

    def __init__(self):
        pass

    def new_cli_client(self, ip, port):
        gui_client = self.new_client(ip, port)
        return gui_client


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
    实现一个简单的消息发布订阅模型用于GUI端和服务端间的交互
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
    print("todo")
