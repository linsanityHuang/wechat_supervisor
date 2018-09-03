import itchat
from itchat.content import *
import sys
from redis_utils import RedisHelper
import os, shutil

def move_file(srcfile,dstfile):
	if not os.path.isfile(srcfile):
		print("%s not exist!"%(srcfile))
	else:
		fpath, fname = os.path.split(dstfile)    #分离文件名和路径
		if not os.path.exists(fpath):
			os.makedirs(fpath)                #创建路径
		shutil.move(srcfile, dstfile)          #移动文件
		print("move %s -> %s"%( srcfile,dstfile))

sys.path.append('./')
obj = RedisHelper()

# 自动回复文本等类别的群聊消息
# isGroupChat=True表示为群聊消息
@itchat.msg_register([TEXT, SHARING], isGroupChat=True)
def group_reply_text(msg):
	# 消息来自于哪个群聊
	chatroom_id = msg['FromUserName']
	# 发送者的昵称
	username = msg['ActualNickName']
	print('username', username)
	# 消息并不是来自于需要同步的群
	if not chatroom_id in chatroom_ids:
		return
	content = ''
	if msg['Type'] == TEXT:
		content = msg['Content']
	elif msg['Type'] == SHARING:
		content = msg['Text']
	content = username + ': ' + content
	if content != '':
		obj.publish('chat_msg', content)


# 自动回复图片等类别的群聊消息
# isGroupChat=True表示为群聊消息
@itchat.msg_register([PICTURE, ATTACHMENT, VIDEO], isGroupChat=True)
def group_reply_media(msg):
	# 消息来自于哪个群聊
	chatroom_id = msg['FromUserName']
	# 发送者的昵称
	username = msg['ActualNickName']

	# 消息并不是来自于需要同步的群
	if not chatroom_id in chatroom_ids:
		return

	# 如果为gif图片则不转发
	if msg['FileName'][-4:] == '.gif':
		return

	# 下载图片等文件
	msg['Text'](msg['FileName'])
	print(msg['FileName'])
	file_name = msg['FileName']
	root_dir = '/Users/huangjiansheng/PycharmProjects/wechat/'
	dest_dir = '/Users/huangjiansheng/PycharmProjects/wechat/static/'
	move_file(root_dir + file_name, dest_dir + file_name)
	obj.publish('chat_msg', 'image:' + file_name)

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
