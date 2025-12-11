# Основной файл для запуска тг-бота
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import BOT_TOKEN
from telegram.error import BadRequest
from handlers import *
import logging

# Включим логирование, чтобы видеть ошибки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок."""
    logger.error(f"Exception while handling update: {context.error}")

    # Игнорируем ошибки BadRequest (часто возникают при редактировании сообщений)
    if isinstance(context.error, BadRequest):
        if "Inline keyboard expected" in str(context.error):
            logger.warning("Ignored: Inline keyboard expected error")
        elif "Can't parse entities" in str(context.error):
            logger.warning("Ignored: Markdown parsing error")
        return

    # Для других ошибок можно отправить сообщение пользователю
    if update and update.effective_message:
        await update.effective_message.reply_text("Произошла ошибка. Попробуйте еще раз.")

def main() -> None:
    """Запуск бота."""
    # Создаем Application и передаем ему токен
    application = Application.builder().token(BOT_TOKEN).build()

    # Обработчики команд
    application.add_error_handler(error_handler)
    application.add_handler(CommandHandler("start", start))

    # Обработчики текстовых сообщений из главного меню
    application.add_handler(MessageHandler(filters.Regex("^Специалисты$"), specialists_main))
    application.add_handler(MessageHandler(filters.Regex("^Услуги$"), services_main))
    application.add_handler(MessageHandler(filters.Regex("^Направления$"), directions_main))
    application.add_handler(MessageHandler(filters.Regex("^Наш сайт$"), website))

    # Обработчики нажатий на inline-кнопки
    application.add_handler(CallbackQueryHandler(button_doctor, pattern="^doctor_"))
    application.add_handler(CallbackQueryHandler(button_service_specialists, pattern="^service_specialists$"))
    application.add_handler(CallbackQueryHandler(button_specialization, pattern="^specialization_"))
    application.add_handler(CallbackQueryHandler(button_service_doctor, pattern="^service_doctor_"))
    application.add_handler(CallbackQueryHandler(button_service_doctor_detail, pattern="^detail_service_doctor_"))
    application.add_handler(CallbackQueryHandler(button_service_procedures, pattern="^service_procedures$"))
    application.add_handler(CallbackQueryHandler(button_procedure, pattern="^procedure_"))
    application.add_handler(CallbackQueryHandler(button_direction, pattern="^direction_"))
    application.add_handler(CallbackQueryHandler(button_direction_detail, pattern="^detail_direction_"))
    application.add_handler(CallbackQueryHandler(button_direction_more_detail, pattern="^more_detail_direction_"))
    application.add_handler(CallbackQueryHandler(button_appointment, pattern="^appointment_"))
    application.add_handler(CallbackQueryHandler(button_back, pattern="^back_"))

    # Запускаем бота (бесконечный опрос серверов Telegram)
    print("Бот запущен...")
    application.run_polling()

# Точка входа
if __name__ == '__main__':
    main()