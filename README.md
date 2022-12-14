# telegram 私聊机器人消息转发到群组 bot

## 功能：

 - 私聊机器人的消息会被bot转发到给定chat_id的群组，并显示私聊人的信息。
 - 在对应群组回复机器人转发的消息会被bot转发给对应的私聊人，实现bot匿名聊天。
 - 回复机器人的消息新增支持图片和图片+文字。
 - 回复机器人的纯文字形式消息支持编辑。

## TODO：
 - `message_id`和`user_id`的对应关系改用数据库存储与处理。
 - 回复机器人的消息适配多种多媒体格式。

## 感谢：
[`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot)
