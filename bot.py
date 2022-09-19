from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler
from telegram import Update, Bot, ParseMode
from telegram.utils.request import Request
import json
import time

CHAT_ID=0 #修改为群聊的chat_id
BOT_TOKEN=0 #修改为bot的token

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        '你好, {}\n接USTC相关投稿\n如果您想投稿请直接发给机器人'.format(update.message.from_user.first_name)
    )

def post_all(update: Update, context: CallbackContext):
    message_id = update.message.message_id
    user = update.message.from_user
    print(user)
    user_info = "*User: *[{}](tg://user?id={})\n*ID: *`{}`.".format(user['first_name'], user['id'], user['id'])
    global USER_ID_MEM
    if(user['id'] != USER_ID_MEM):
        context.bot.send_message(chat_id=CHAT_ID, text=user_info, parse_mode=ParseMode.MARKDOWN)
        USER_ID_MEM = user['id']
    try:
        fwd_message = context.bot.forward_message(chat_id=CHAT_ID, 
        from_chat_id=update.effective_chat.id, 
        message_id=update.message.message_id)
    except Exception as e:
        print(e)
        return
    global MSGID_to_UID
    MSGID_to_UID[str(fwd_message.message_id)] = [user['id'], message_id]
    

def post_return(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if(chat_id != CHAT_ID):
        return
    else:
        reply = update.message.reply_to_message
        #print(update.message.text_markdown_v2)
        message_id = reply['message_id']
        current_message_id = update.message.message_id
        try:
            global MSGID_to_UID
            print(MSGID_to_UID)
            userid, fwdmsg_id = MSGID_to_UID[str(message_id)]
        except Exception as e:
            print(e)
            return
            #context.bot.send_message(chat_id=CHAT_ID, text="找不到转发来源.", reply_to_message_id=message_id)
        context.bot.send_message(chat_id=userid, text=update.message.text_markdown_v2, parse_mode=ParseMode.MARKDOWN_V2)
        retmsg = context.bot.send_message(chat_id=CHAT_ID, text="已发送.")#, reply_to_message_id=current_message_id)
        time.sleep(1)
        context.bot.delete_message(chat_id=CHAT_ID, message_id=retmsg.message_id)


print("starting...")
USER_ID_MEM = ""
MSGID_to_UID = dict()
file_open = open("msg_to_user.json", "r")
js_read = file_open.read()
try:
    MSGID_to_UID = json.loads(js_read)
except Exception as e:
    print(e)
    MSGID_to_UID = dict()
file_open.close()
print("started.")

updater = Updater(BOT_TOKEN)
updater.dispatcher.add_handler(CommandHandler('start', start))
#updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), post_text))
#updater.dispatcher.add_handler(MessageHandler(Filters.photo, post_photo))
updater.dispatcher.add_handler(MessageHandler(Filters.all & Filters.chat_type.private & (~Filters.command), post_all))
updater.dispatcher.add_handler(MessageHandler(Filters.reply, post_return))
updater.start_polling()
updater.idle()

print("stopping...")
js_store = json.dumps(MSGID_to_UID)
file = open("msg_to_user.json", 'w')
file.write(js_store)
file.close()
print("stopped.")