# 微信群聊游戏

目前只有一个成语接龙

实现原理，爬虫获取成语数据

参考https://github.com/pwxcoo/chinese-xinhua

利用itChat实现python微信回调

利用tuling机器人，实现ai聊天机器人

## 环境配置
pip 安装

python 安装

pip 安装 itChat

pip 安装 request

需要去图灵机器人官网申请一个KEY，替换tuling_replay.py中的KEY

http://www.tuling123.com/member/robot/index.jhtml

其他的话，看提示缺啥就安装啥吧，没什么特殊丶库,pip都可以搞定
## 成语接龙

python tuling_reply.py
### 游戏规则:	
1.	在群聊中输入[成语接龙]， 开始游戏
2. 根据随机产生的成语，进行成语接龙游戏
3. 答对10次，有戏结束
4. 输入错误的成语，会提示
