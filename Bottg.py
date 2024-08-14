import telebot
from datetime import timedelta
import time

API_TOKEN = '6883001396:AAEbGBMpzfCjbzYXUBW8jPefiqUhoO1ixv4'
bot = telebot.TeleBot(API_TOKEN)

# Список администраторов
admins = [6321157988]

# Словарь для хранения временных ограничений пользователей
muted_users = {}
banned_users = {}

# Проверка, является ли пользователь администратором
def is_admin(user_id):
    return user_id in admins

# Команда для добавления администратора
@bot.message_handler(commands=['addadm'])
def add_admin(message):
    if is_admin(message.from_user.id):
        new_admin_id = message.text.split()[1]
        if new_admin_id.isdigit():
            admins.append(int(new_admin_id))
            bot.reply_to(message, f'Пользователь {new_admin_id} добавлен как администратор.')
        else:
            bot.reply_to(message, "ID администратора должен быть числом.")
    else:
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")

# Команда для мута
@bot.message_handler(commands=['mute'])
def mute_user(message):
    if is_admin(message.from_user.id):
        user_id = message.text.split()[1]
        time_in_seconds = int(message.text.split()[2])
        muted_users[int(user_id)] = time.time() + time_in_seconds
        bot.reply_to(message, f'Пользователь {user_id} замучен на {time_in_seconds} секунд.')
    else:
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")

# Команда для бана
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if is_admin(message.from_user.id):
        user_id = message.text.split()[1]
        time_in_seconds = int(message.text.split()[2])
        banned_users[int(user_id)] = time.time() + time_in_seconds
        bot.reply_to(message, f'Пользователь {user_id} забанен на {time_in_seconds} секунд.')
    else:
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")

# Проверка мута и бана
def check_mutes_and_bans():
    current_time = time.time()
    
    # Удаляем пользователей, чей мут истек
    for user_id in list(muted_users.keys()):
        if current_time > muted_users[user_id]:
            del muted_users[user_id]
    
    # Удаляем пользователей, чей бан истек
    for user_id in list(banned_users.keys()):
        if current_time > banned_users[user_id]:
            del banned_users[user_id]

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.from_user.id in muted_users:
        bot.reply_to(message, "Вы замучены и не можете отправлять сообщения.")
        return
    if message.from_user.id in banned_users:
        bot.reply_to(message, "Вы забанены и не можете отправлять сообщения.")
        return

# Запуск бота
if __name__ == '__main__':
    while True:
        check_mutes_and_bans()
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            time.sleep(15)
