import telebot
from telebot import types
import time

# Инициализация бота
TOKEN = "6883001396:AAEbGBMpzfCjbzYXUBW8jPefiqUhoO1ixv4"
bot = telebot.TeleBot(TOKEN)

# Список администраторов
admins = set([7069906494])

# Хранение состояний пользователей
mute_status = {}
banned_users = {}
warn_count = {}

# Команда для добавления администраторов
@bot.message_handler(commands=['addadm'])
def add_admin(message):
    if message.from_user.id in admins:
        try:
            new_admin_id = int(message.text.split()[1])
            admins.add(new_admin_id)
            bot.reply_to(message, f"Пользователь {new_admin_id} добавлен в администраторы.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /addadm <user_id>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для мута
@bot.message_handler(commands=['mute'])
def mute(message):
    if message.from_user.id in admins:
        try:
            user_id = int(message.text.split()[1])
            duration = int(message.text.split()[2])
            mute_status[user_id] = (time.time() + duration)
            bot.reply_to(message, f"Пользователь {user_id} был замучен на {duration} секунд.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /mute <user_id> <duration>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для размута
@bot.message_handler(commands=['unmute'])
def unmute(message):
    if message.from_user.id in admins:
        try:
            user_id = int(message.text.split()[1])
            if user_id in mute_status:
                del mute_status[user_id]
                bot.reply_to(message, f"Пользователь {user_id} был размучен.")
            else:
                bot.reply_to(message, f"Пользователь {user_id} не замучен.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /unmute <user_id>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для бана
@bot.message_handler(commands=['ban'])
def ban(message):
    if message.from_user.id in admins:
        try:
            user_id = int(message.text.split()[1])
            duration = int(message.text.split()[2])
            banned_users[user_id] = (time.time() + duration)
            bot.reply_to(message, f"Пользователь {user_id} был забанен на {duration} секунд.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /ban <user_id> <duration>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для разбанивания
@bot.message_handler(commands=['unban'])
def unban(message):
    if message.from_user.id in admins:
        try:
            user_id = int(message.text.split()[1])
            if user_id in banned_users:
                del banned_users[user_id]
                bot.reply_to(message, f"Пользователь {user_id} был разбанен.")
            else:
                bot.reply_to(message, f"Пользователь {user_id} не забанен.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /unban <user_id>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для варна
@bot.message_handler(commands=['warn'])
def warn(message):
    if message.from_user.id in admins:
        try:
            user_id = int(message.text.split()[1])
            warn_count[user_id] = warn_count.get(user_id, 0) + 1
            bot.reply_to(message, f"Пользователь {user_id} получил варн. Всего варнов: {warn_count[user_id]}")
            
            # Проверка на три варна
            if warn_count[user_id] >= 3:
                ban_duration = 31536000  # Например, 1 час
                banned_users[user_id] = (time.time() + ban_duration)
                bot.reply_to(message, f"Пользователь {user_id} был забанен на 1 год за 3 варна.")
                del warn_count[user_id]  # Сбросить счетчик варнов
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /warn <user_id>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Команда для кика
@bot.message_handler(commands=['kick'])
def kick(message):
    if message.from_user.id in admins:
        try:
            user_id = int(message.text.split()[1])
            bot.kick_chat_member(message.chat.id, user_id)
            bot.reply_to(message, f"Пользователь {user_id} был кикнут из чата.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Используйте: /kick <user_id>")
    else:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")

# Проверка состояний пользователей
@bot.message_handler(func=lambda message: True)
def check_user_status(message):
    user_id = message.from_user.id

    # Проверка мута
    if user_id in mute_status:
        if time.time() < mute_status[user_id]:
            bot.delete_message(message.chat.id, message.message_id)
            return
        else:
            del mute_status[user_id]

    # Проверка бана
    if user_id in banned_users:
        if time.time() < banned_users[user_id]:
            bot.kick_chat_member(message.chat.id, user_id)
            return
        else:
            del banned_users[user_id]

# Запуск бота
bot.polling(none_stop=True)
