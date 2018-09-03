import json
from flask import Flask, render_template
from flask_socketio import SocketIO
from redis_utils import RedisHelper

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None

forbiden_name_list = []

# 一个后台线程，持续接收redis消息，并发送给客户端浏览器
def background_thread():
	obj = RedisHelper()
	redis_sub = obj.subscribe('chat_msg')  # 调用订阅方法
	while True:
		msg = redis_sub.parse_response()
		print('msg', msg)
		username = msg[2].split(':')[0]
		if username in forbiden_name_list:
			return
		socketio.emit('test_message', {'data': msg[2]})

# 客户端发送connect事件时的处理函数
@socketio.on('test_connect')
def connect(message):
	print(message)
	global thread
	if thread is None:
		# 单独开启一个线程给客户端发送数据
		thread = socketio.start_background_task(target=background_thread)
	socketio.emit('connected', {'data': forbiden_name_list})


# 通过访问http://127.0.0.1:5000/访问index.html
@app.route("/")
def handle_mes():
	return render_template("index.html", forbiden_name_list=forbiden_name_list)

@app.route('/forbiden_name/<username>')
def forbiden_name(username):
	global forbiden_name_list
	print('username', username)
	if username is not None:
		forbiden_name_list.append(username)
	result = dict(
			status='success',
			data=tuple(forbiden_name_list),
		)
	return json.dumps(result, ensure_ascii=False)

# main函数
if __name__ == '__main__':
	socketio.run(app, debug=True)
