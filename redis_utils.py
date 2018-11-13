import redis
import time


class RedisHelper(object):
	def __init__(self):
		# self.__conn = redis.Redis(host='192.168.21.61',port=6379, password='123456Hb')#连接Redis
		self.__conn = redis.Redis(host='127.0.0.1', port=6379, db=1, decode_responses=True)

	def publish(self, channel, msg):
		'''
		channel: 指定消息发送的频道
		msg: 消息内容
		'''
		self.__conn.publish(channel, msg)
		return True

	def subscribe(self, channel):
		'''
		channel: 指定接收消息的频道
		'''
		pub = self.__conn.pubsub()
		pub.subscribe(channel)
		pub.parse_response()
		return pub

	def rpush(self, name, value):
		'''
		把微信用户发送的消息存在一个list的右端
		'''
		self.__conn.rpush(name, value)
		return True

	def lrange(self, name):
		'''
		获取历史消息列表
		'''
		return self.__conn.lrange(name, 0, -1)

	def sadd(self, name, value):
		'''
		添加用户名到set集合
		'''
		self.__conn.sadd(name, value)
		return True

	def smembers(self, name):
		'''
		获取集合的元素
		'''
		return self.__conn.smembers(name)

	def sismember(self, name, value):
		'''
		判断是否是集合的成员
		'''
		return self.__conn.sismember(name, value)

	def srem(self, name, value):
		'''
		删除集合中的元素
		'''
		self.__conn.srem(name, value)
		return True


if __name__ == '__main__':
	obj = RedisHelper()

	# while True:
	# 	time.sleep(1)
	# 	print('publish')
	# 	obj.publish('test1', '你哈')
	obj.rpush('history_msg', ['huang', 'ahah'])

	result = obj.lrange('history_msg')
	import json
	for item in result:
		print(item)
		print(type(item))
