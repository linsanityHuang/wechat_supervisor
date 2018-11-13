import itchat
from itchat.content import *
import sys
from redis_utils import RedisHelper
import json

sys.path.append('./')
obj = RedisHelper()


# 自动回复文本等类别的群聊消息
# isGroupChat=True表示为群聊消息
@itchat.msg_register([TEXT], isGroupChat=True)
def group_reply_text(msg):
	try:
		# print(msg)
		# 群昵称
		chatroom_name = msg['User']['NickName']
		# print(chatroom_name)
		# 消息来自于哪个群聊
		chatroom_id = msg['FromUserName']
		# 发送者的昵称
		username = msg['ActualNickName']
		if username == '':
			username = msg['User']['Self']['NickName']
		# 消息并不是来自于需要同步的群
		if not chatroom_id in chatroom_ids:
			return
		content = msg['Content']
		print(username, content)
		chat_msg = dict(
				chatroom_name=chatroom_name,
				msg_type=msg['Type'],
				username=username,
				content=content,
			)
		obj.publish('chat_msg', json.dumps(chat_msg))
	except Exception as e:
		raise e


# 扫二维码登录
itchat.auto_login(hotReload=True)
# 获取所有通讯录中的群聊
# 需要在微信中将需要同步的群聊都保存至通讯录
# chatrooms = itchat.get_chatrooms(update=True, contactOnly=True)
chatrooms = itchat.get_chatrooms(update=True)
chatroom_ids = [c['UserName'] for c in chatrooms]
print('正在监测的群聊：', len(chatrooms), '个')
print(' '.join([item['NickName'] for item in chatrooms]))
itchat.run()
