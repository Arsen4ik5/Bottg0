import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.utils.request import Request

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up bot token and admin ID
TOKEN = '6883001396:AAEbGBMpzfCjbzYXUBW8jPefiqUhoO1ixv4'
ADMIN_ID = 7069906494

# Initialize bot
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hello! I\'m a bot.')

def add_admin(update, context):
    if update.message.from_user.id == ADMIN_ID:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Admin added.')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Access denied.')

def ban_user(update, context):
    if update.message.from_user.id == ADMIN_ID:
        user_id = update.message.reply_to_message.from_user.id
        context.bot.kick_chat_member(update.effective_chat.id, user_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'User {user_id} banned.')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Access denied.')

def unmute_user(update, context):
    if update.message.from_user.id == ADMIN_ID:
        user_id = update.message.reply_to_message.from_user.id
        context.bot.unban_chat_member(update.effective_chat.id, user_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'User {user_id} unmuted.')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Access denied.')

def mute_user(update, context):
    if update.message.from_user.id == ADMIN_ID:
        user_id = update.message.reply_to_message.from_user.id
        duration = int(context.args[0])
        context.bot.restrict_chat_member(update.effective_chat.id, user_id, permissions={'can_send_messages': False}, until_date=update.timestamp + duration)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'User {user_id} muted for {duration} seconds.')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Access denied.')

def warn_user(update, context):
    if update.message.from_user.id == ADMIN_ID:
        user_id = update.message.reply_to_message.from_user.id
        message_text = update.message.text
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'User {user_id} warned: {message_text}')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Access denied.')

def main():
    # Create the bot
    updater = Updater(TOKEN, request_kwargs={'read_timeout': 30})

    # Add handlers
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('addadm', add_admin))
    updater.dispatcher.add_handler(CommandHandler('ban', ban_user))
    updater.dispatcher.add_handler(CommandHandler('unmute', unmute_user))
    updater.dispatcher.add_handler(CommandHandler('mute', mute_user))
    updater.dispatcher.add_handler(CommandHandler('warn', warn_user))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
