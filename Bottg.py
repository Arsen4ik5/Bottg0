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

# ... (другие ваши асинхронные функции)

async def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    # Загрузка администраторов из базы данных
    for admin in session.query(Admin).all():
        admins.add(admin.user_id)

    application.add_handler(CommandHandler("start", start))
    # ... (добавьте другие обработчики)

    await application.run_polling()

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    asyncio.run(main())
