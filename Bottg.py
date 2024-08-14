import logging
from telegram.ext import Updater, CommandHandler, MessageHandler

logging.basicConfig(level=logging.INFO)

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'  # Получите токен вашего бота

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Привет! Я - твой новый бот.')

def addadm(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    if context.bot.get_chat_administrators(chat_id).get(user_id):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Вы успешно назначены админом.')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Вы не администратор в этой группе.')

def ban(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    if context.bot.get_chat_administrators(chat_id).get(user_id):
        member = update.effective_message.from_user
        context.bot.kick_chat_member(chat_id=chat_id, user_id=member.id)
        context.bot.send_message(chat_id=chat_id, text='Пользователь banned.')
    else:
        context.bot.send_message(chat_id=chat_id, text='Вы не администратор в этой группе.')

def mute(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    if context.bot.get_chat_administrators(chat_id).get(user_id):
        member = update.effective_message.from_user
        context.bot.restrict_chat_member(chat_id=chat_id, user_id=member.id, permissions=telegram.ChatPermissions())
        context.bot.send_message(chat_id=chat_id, text='Пользователь muted.')
    else:
        context.bot.send_message(chat_id=chat_id, text='Вы не администратор в этой группе.')

def warn(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    if context.bot.get_chat_administrators(chat_id).get(user_id):
        member = update.effective_message.from_user
        context.bot.send_message(chat_id=chat_id, text='Варн пользователя.', reply_to_message_id=update.effective_message.message_id)
    else:
        context.bot.send_message(chat_id=chat_id, text='Вы не администратор в этой группе.')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('addadm', addadm))
    dp.add_handler(CommandHandler('ban', ban))
    dp.add_handler(CommandHandler('mute', mute))
    dp.add_handler(CommandHandler('warn', warn))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
