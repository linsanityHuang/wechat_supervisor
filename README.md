# 项目介绍

##核心功能
1. 把微信内的群消息实时展示在web页面，只同步了文本消息，并且过滤了重复的消息
2. 支持屏蔽用户和取消屏蔽用户

##技术构成
1. Flask
2. itchat
3. Redis

##功能详解
1. 微信消息到web服务器是通过Redis的发布和订阅功能实现的
2. 消息从web服务器到页面上是通过socketio实现的
3. 登录微信使用的是第三方依赖itchat，官方主页：

##参考资料
1. itchat，官方主页：https://itchat.readthedocs.io/zh/latest/
2. https://www.jianshu.com/p/7aeadca0c9bd
3. https://www.pyfdtic.com/2018/03/16/python-itchat-weixin-api/

##部署步骤
1. python 3.6.6
2. pip install -r requirements.txt
3. redis
4. cd wechat_supervisor
5. python itchat_utils.py 扫码登录微信
6. python app.py 启动web服务
7. 访问http://127.0.0.1:5000/
