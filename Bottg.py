import logging
from telegram.ext import Updater, CommandHandler, MessageHandle
# Enable logging
logging.basicConfig(level=logging.INFO)

# Define the bot token
TOKEN = '6883001396:AAEbGBMpzfCjbzYXUBW8jPefiqUhoO1ixv4'

# Define the administrator IDs
ADMINS = [7069906494]

# Define the commands
@bot.command('/ban')
def ban_command(update, context):
    if context.effective_user.id in ADMINS:
        user_id = update.effective_message.text.split()[1]
        ban_time = int(update.effective_message.text.split()[2])
        bot.ban_chat_member(update.effective_chat.id, user_id, ban_time)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'User {user_id} banned for {ban_time} seconds.')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Only administrators can use this command.')

@bot.command('/mute')
def mute_command(update, context):
    if context.effective_user.id in ADMINS:
        user_id = update.effective_message.text.split()[1]
        mute_time = int(update.effective_message.text.split()[2])
        bot.restrict_chat_member(update.effective_chat.id, user_id, mute_time)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'User {user_id} muted for {mute_time} seconds.')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Only administrators can use this command.')

@bot.command('/warn')
def warn_command(update, context):
    if context.effective_user.id in ADMINS:
        user_id = update.effective_message.text.split()[1]
        message = update.effective_message.text.split()[2]
        bot.send_message(chat_id=user_id, text=message)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'User {user_id} warned: {message}.')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Only administrators can use this command.')

# Define the message handlers
@bot.message('/')
def message_handler(update, context):
    if context.effective_user.id in ADMINS:
        # Handle messages from administrators
        pass
    else:
        # Handle messages from regular users
        pass

# Start the bot
bot.start_polling()
