import json
from flask import Flask, render_template
from flask_socketio import SocketIO
from redis_utils import RedisHelper

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None

forbiden_names = []
redis = RedisHelper()


# 一个后台线程，持续接收redis消息，并发送给客户端浏览器
def background_thread():
	redis_sub = redis.subscribe('chat_msg')  # 调用订阅方法
	while True:
		# time.sleep(1)
		msg = redis_sub.parse_response()
		chat_msg = json.loads(msg[2])
		print('chat_msg', chat_msg)
		# {'chatroom_name': '搞事三人行', 'msg_type': 'Text', 'username': '', 'content': '来来来'}
		username = chat_msg['username']
		if redis.sismember('forbiden_names', username):
			continue
		# 过滤重复消息
		# 只根据用户发送的消息过滤
		contents = redis.lrange('wechat_msg')
		# print(contents)
		if chat_msg['content'] in contents:
			continue
		# 已发送的消息放在判断重复的集合中
		# 把用户的名称放进去，加载历史消息的时候展示
		redis.rpush('wechat_msg', chat_msg['content'])
		socketio.emit('test_message', {'data': chat_msg})
		with open('history_msg.txt', 'a+', encoding='utf-8') as f:
			f.writelines(username + ': ' + chat_msg['content'] +'\n')


# 客户端发送connect事件时的处理函数
@socketio.on('test_connect')
def connect(message):
	print(message)
	global thread
	if thread is None:
		# 单独开启一个线程给客户端发送数据
		thread = socketio.start_background_task(target=background_thread)
	socketio.emit('connected', {'data': forbiden_names})


# 通过访问http://127.0.0.1:5000/访问index.html
@app.route("/")
def handle_mes():
	# 访问首页的时候从Redis中获取历史消息，加载到页面上
	forbiden_names = redis.smembers('forbiden_names')
	return render_template("index.html", forbiden_names=forbiden_names)


# 屏蔽用户消息
@app.route('/forbiden_name/<username>')
def forbiden_name(username):
	print('username', username)
	if username is not None and not redis.sismember('forbiden_names', username):
		redis.sadd('forbiden_names', username)
	forbiden_names = redis.smembers('forbiden_names')
	result = dict(
			status='success',
			data=tuple(forbiden_names),
		)
	return json.dumps(result, ensure_ascii=False)


# 取消屏蔽
@app.route('/unforbiden_name/<username>')
def unforbiden_name(username):
	print('username', username)
	if username is not None and redis.sismember('forbiden_names', username):
		redis.srem('forbiden_names', username)
	forbiden_names = redis.smembers('forbiden_names')
	result = dict(
			status='success',
			data=tuple(forbiden_names),
		)
	return json.dumps(result, ensure_ascii=False)


# main函数
if __name__ == '__main__':
	socketio.run(app, debug=True)
