import telebot

bot = telebot.TeleBot("6883001396:AAEbGBMpzfCjbzYXUBW8jPefiqUhoO1ixv4")

admins = [7069906494]

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['addadm'])
def add_admin(message):
    admins.append(message.chat.id)
    bot.send_message(message.chat.id, "Вы добавлены в список администраторов.")

@bot.message_handler(func=lambda message: message.chat.id in admins, commands=['ban'])
def ban_user(message):
    user_id = message.text.split(' ')[1]
    bot.send_message(message.chat.id, f"Пользователь {user_id} забанен.")

@bot.message_handler(func=lambda message: message.chat.id in admins, commands=['mute'])
def mute_user(message):
    user_id = message.text.split(' ')[1]
    bot.send_message(message.chat.id, f"Пользователь {user_id} замучен.")

@bot.message_handler(func=lambda message: message.chat.id in admins, commands=['warn'])
def warn_user(message):
    user_id = message.text.split(' ')[1]
    bot.send_message(message.chat.id, f"Пользователю {user_id} выдан варн.")

bot.polling()

