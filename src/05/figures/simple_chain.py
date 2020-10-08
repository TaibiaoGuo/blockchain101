# -*- coding: utf-8 -*-
""" Code written entirely by Eric Alcaide & Taibiao Guo.

	blockchain101 实验课内容

	一个简单区块链，其中每个区块都指向上一个区块。这是一个区块链的基本的实现，不包含工作证明或点对点等高级功能。
"""

import datetime
import hashlib
import time

class Message:
	def __init__(self, data):
		self.hash = None
		self.prev_hash = None
		self.timestamp = time.time()
		self.size = len(data.encode('utf-8'))   # length in bytes
		self.data = data
		self.payload_hash = self._hash_payload()

	def _hash_payload(self):
		return hashlib.sha256(bytearray(str(self.timestamp) + str(self.data), "utf-8")).hexdigest()

	def _hash_message(self):
		"""
		组合前一个区块链的哈希 prev_hash 和 当前区块的哈希 _hash_payload 进行sha256运算生成哈希值
		"""
		return hashlib.sha256(bytearray(str(self.prev_hash) + self.payload_hash, "utf-8")).hexdigest()

	def link(self, message):
		""" 将前一个消息和后一个消息间通过哈希进行连接. """
		self.prev_hash = message.hash

	def seal(self):
		""" 获取消息的哈希值. """
		self.hash = self._hash_message()

	def validate(self):
		""" 检查消息是否有效 """
		if self.payload_hash != self._hash_payload():
			raise InvalidMessage("Invalid payload hash in message: " + str(self))
		if self.hash != self._hash_message():
			raise InvalidMessage("Invalid message hash in message: " + str(self))

	def __repr__(self):
		return 'Message<hash: {}, prev_hash: {}, data: {}>'.format(
			self.hash, self.prev_hash, self.data[:20]
		)


class Block:
	def __init__(self, *args):
		self.messages = []
		self.timestamp = None
		self.prev_hash = None
		self.hash = None
		if args:
			for arg in args:
				self.add_message(arg)

	def _hash_block(self):
		return hashlib.sha256(bytearray(str(self.prev_hash) + str(self.timestamp) + self.messages[-1].hash, "utf-8")).hexdigest()

	def add_message(self, message):
		if len(self.messages) > 0:
			message.link(self.messages[-1])
		message.seal()
		message.validate()
		self.messages.append(message)
 
	def link(self, block):
		self.prev_hash = block.hash
        
	def seal(self):
		self.timestamp = time.time()
		self.hash = self._hash_block()

	def validate(self):
		""" 通过调用每条消息的 validate() 方法。验证每个消息的哈希，然后验证链的完整性，最后验证块的哈希。

			如果消息验证失败，此方法将捕获异常并抛出 InvalidBlock， 因为无效的消息会让整个区块无效。
		"""
		for i, msg in enumerate(self.messages):
			try:
				msg.validate()
				if i > 0 and msg.prev_hash != self.messages[i-1].hash:
					raise InvalidBlock("无效区块: Message #{} has invalid message link in block: {}".format(i, str(self)))
			except InvalidMessage as ex:
				raise InvalidBlock("Invalid block: Message #{} failed validation: {}. In block: {}".format(
					i, str(ex), str(self))
				)

	def __repr__(self):
		return '区块<哈希值: {}, 前一个哈希值: {}, 消息数量: {}, 时间戳: {}>'.format(
			self.hash, self.prev_hash, len(self.messages), self.timestamp
		)

class SimpleChain:
	def __init__(self):
		self.chain = []

	def add_block(self, block):
		""" 添加被验证有效的区块."""
		if len(self.chain) > 0:
			block.prev_hash = self.chain[-1].hash
		block.seal()
		block.validate()
		self.chain.append(block)

	def validate(self):
		""" 依次验证每个区块，无效的区块会让链失效。
		"""
		for i, block in enumerate(self.chain):
			try:
				block.validate()
			except InvalidBlock as exc:
				raise InvalidBlockchain("区块链在区块高度 {} 处失效， 因为: {}".format(i, str(exc)))
		return True

	def __repr__(self):
		return 'SimpleChain<blocks: {}>'.format(len(self.chain))


class InvalidMessage(Exception):
	def __init__(self,*args,**kwargs):
		Exception.__init__(self,*args,**kwargs)

class InvalidBlock(Exception):
	def __init__(self,*args,**kwargs):
		Exception.__init__(self,*args,**kwargs)

class InvalidBlockchain(Exception):
	def __init__(self,*args,**kwargs):
		Exception.__init__(self,*args,**kwargs)


def manager():
	chain = SimpleChain()
	block = Block()
	msg = """
                区块链功能的基本实现，可以通过动作集对区块链进行操作。

		动作集:
			- 将消息添加到现有区块  (1)
                        - 将现有块添加到链      (2)
                        - 显示整个区块链        (3)
                        - 显示一个区块          (4)
                        - 验证区块链的完整性    (5)
                        - 退出程序              (6)

                如果完整性受到威胁，则验证动作将终止程序。
		"""

	print(msg)	
	while True:
		print()

		decide = input("选择一个动作: ")

		if decide == "1":
			block.add_message(Message(input("输入你的消息，按回车（Enter）结束输入:")))
		elif decide == "2":
			if len(block.messages) > 0:
				chain.add_block(block)
				block = Block()
			else: print("没有区块，先尝试添加一个消息吧")
		elif decide == "3":
			for b in chain.chain:
				print(b)
				print("----------------")
		elif decide == "4":
			index = int(input("请提供区块索引: "))
			if len(chain.chain)>0:
				try: print(chain.chain[index])
				except: print("发生了一个错误")
		elif decide == "5":
			if chain.validate(): print("区块链通过完整性验证.")
		else:
			break

if __name__ == "__main__":
	manager()
