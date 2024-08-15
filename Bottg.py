import logging
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка базы данных
Base = declarative_base()
engine = create_engine('sqlite:///admins.db')
Session = sessionmaker(bind=engine)
session = Session()

class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True)

Base.metadata.create_all(engine)

# Подключение к Telegram API
TOKEN = '6883001396:AAEbGBMpzfCjbzYXUBW8jPefiqUhoO1ixv4'

# Список администраторов
admins = {6321157988}  # Добавьте своего администратора

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Бот запущен!')

async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in admins:
        await update.message.reply_text('У вас нет прав для добавления администраторов.')
        return

    if context.args:
        try:
            user_id = int(context.args[0])
            new_admin = Admin(user_id=user_id)
            
            session.add(new_admin)
            session.commit()
            admins.add(user_id)
            
            await update.message.reply_text(f'Пользователь {user_id} добавлен как администратор.')
        except ValueError:
            await update.message.reply_text('Неверный формат user_id. Убедитесь, что это число.')
        except Exception as e:
            logger.error(e)
            await update.message.reply_text('Ошибка при добавлении администратора.')
    else:
        await update.message.reply_text('Используйте: /addadm <user_id>')

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in admins or not context.args:
        await update.message.reply_text('У вас нет прав для использования этой команды.')
        return

    try:
        user_id = int(context.args[0])
        duration = int(context.args[1]) if len(context.args) > 1 else 60  # По умолчанию мут на 60 секунд

        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=update.message.date.timestamp() + duration
        )
        await update.message.reply_text(f'Пользователь {user_id} замучен на {duration} секунд.')
    except (ValueError, IndexError):
        await update.message.reply_text('Используйте: /mute <user_id> [duration]')
    except Exception as e:
        logger.error(e)
        await update.message.reply_text('Не удалось замутить пользователя.')

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in admins or not context.args:
        await update.message.reply_text('У вас нет прав для использования этой команды.')
        return

    try:
        user_id = int(context.args[0])
        duration = int(context.args[1]) if len(context.args) > 1 else 60  # По умолчанию кик на 60 секунд

        await context.bot.kick_chat_member(chat_id=update.effective_chat.id, user_id=user_id)

        # Сообщение для возвращения пользователя
        await asyncio.sleep(duration)
        await context.bot.unban_chat_member(chat_id=update.effective_chat.id, user_id=user_id)
        await update.message.reply_text(f'Пользователь {user_id} кикнут на {duration} секунд и возвращен.')

    except (ValueError, IndexError):
        await update.message.reply_text('Используйте: /kick <user_id> [duration]')
    except Exception as e:
        logger.error(e)
        await update.message.reply_text('Не удалось кикнуть пользователя.')

async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in admins or not context.args:
        await update.message.reply_text('У вас нет прав для использования этой команды.')
        return

    try:
        user_id = int(context.args[0])
        await update.message.reply_text(f'Пользователь {user_id} получил варн.')
    except ValueError:
        await update.message.reply_text('Неверный формат user_id. Убедитесь, что это число.')

async def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    # Загрузка администраторов из базы данных
    for admin in session.query(Admin).all():
        admins.add(admin.user_id)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("addadm", add_admin))
    application.add_handler(CommandHandler("mute", mute))
    application.add_handler(CommandHandler("kick", kick))
    application.add_handler(CommandHandler("warn", warn))

    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
