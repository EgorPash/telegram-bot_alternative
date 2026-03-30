# Файл с обработчиками команд и сообщений
import datetime
import logging
import os
from aiogram.types import update
from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes, ConversationHandler
import json
from keyboards import *

logger = logging.getLogger(__name__)

# Состояния
NAME, PHONE, DAY = range(3)

# Загружаем данные из JSON
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = data['start_message']
    clinic_images = data['clinic_images']
    contact_numbers = data['contact_numbers']

    # Отправляем приветственное сообщение
    await update.message.reply_text(welcome_text)

    # Отправляем фотографии из clinic_images
    for image_path in clinic_images:
        if os.path.exists(image_path):
            with open(image_path, 'rb') as photo:
                await update.message.reply_photo(photo=photo)
        else:
            logger.warning(f"Фото не найдено: {image_path}")

    # Отправляем контактные номера
    await update.message.reply_text(contact_numbers)

    # Отправляем главное меню
    keyboard = main_menu_keyboard()
    await update.message.reply_text("Главное меню:", reply_markup=keyboard)

# Обработчик текстового сообщения "Специалисты" (из главного меню)
async def specialists_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = data['specialists']['title']
    keyboard = specialists_keyboard()
    await update.message.reply_text(text, reply_markup=keyboard)

# Обработчик текстового сообщения "Услуги"
async def services_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = data['services']['title']
    keyboard = services_keyboard()
    await update.message.reply_text(text, reply_markup=keyboard)

# Обработчик текстового сообщения "Направления"
async def directions_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = data['directions']['title']
    keyboard = directions_keyboard()
    await update.message.reply_text(text, reply_markup=keyboard)

# Обработчик текстового сообщения "Наш сайт"
async def website(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Наш сайт: https://alternative-clinic.ru")

# --- Обработчики CallbackQuery (нажатия на inline-кнопки) ---

# Обработчик выбора врача из специалистов (главное меню)
async def button_doctor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    doctor_key = query.data.replace('doctor_', '')
    doctor_data = data['specialists']['doctors'][doctor_key]
    photo_path = doctor_data.get('photo')
    text = f"*{doctor_data['name']}*\nСпециализация: {doctor_data['specialization']}"
    keyboard = doctor_detail_keyboard(doctor_key)
    if photo_path and os.path.exists(photo_path):
        with open(photo_path, 'rb') as photo:
            await query.message.reply_photo(
                photo=photo,
                caption=text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        await query.message.delete()
    else:
        await query.edit_message_text(
            text + "\n\n📷 *Фотография не найдена*",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )

# Обработчик выбора "Специалисты" внутри "Услуг"
async def button_service_specialists(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "Выберите специализацию:"
    keyboard = service_specializations_keyboard()
    await query.edit_message_text(text, reply_markup=keyboard)

# Обработчик выбора специализации внутри услуг
async def button_specialization(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    specialization_key = query.data.replace('specialization_', '')
    context.user_data['current_specialization'] = specialization_key  # Сохраняем контекст
    specialization_data = data['specializations'][specialization_key]
    text = f"Выберите врача ({specialization_data['title']}):"
    keyboard = service_specialists_keyboard(specialization_key)
    await query.edit_message_text(text, reply_markup=keyboard)

# Обработчик выбора врача из услуг
async def button_service_doctor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    doctor_key = query.data.replace('service_doctor_', '')

    # Получаем текущую специализацию из контекста
    current_specialization = context.user_data.get('current_specialization')

    if not current_specialization:
        await query.edit_message_text("Ошибка: не определена специализация. Пожалуйста, начните сначала.")
        return

    doctor_data = None
    specialization = data['specializations'].get(current_specialization)
    if specialization and doctor_key in specialization['doctors']:
        doctor_data = specialization['doctors'][doctor_key]

    if doctor_data:
        photo_path = doctor_data.get('photo')
        text = f"*{doctor_data['name']}*\nСпециализация: {doctor_data['specialization']}"
        keyboard = service_doctor_detail_keyboard(doctor_key)
        if photo_path and os.path.exists(photo_path):
            with open(photo_path, 'rb') as photo:
                await query.message.reply_photo(
                    photo=photo,
                    caption=text,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
            await query.message.delete()
        else:
            await query.edit_message_text(
                text + "\n\n📷 *Фотография не найдена*",
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
    else:
        await query.edit_message_text("Данные о враче не найдены.")

# Обработчик кнопки "Подробнее" о враче из услуг
async def button_service_doctor_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    doctor_key = query.data.replace('detail_service_doctor_', '')

    current_specialization = context.user_data.get('current_specialization')
    if not current_specialization:
        await query.edit_message_text("Ошибка: не определена специализация. Пожалуйста, начните сначала.")
        return

    doctor_data = None
    specialization = data['specializations'].get(current_specialization)
    if specialization and doctor_key in specialization['doctors']:
        doctor_data = specialization['doctors'][doctor_key]

    if doctor_data:
        photo_path = doctor_data.get('photo')
        text = f"*{doctor_data['name']}*\nСпециализация: {doctor_data['specialization']}\n\n{doctor_data['description']}"
        keyboard = service_doctor_description_keyboard(doctor_key)
        if photo_path and os.path.exists(photo_path):
            with open(photo_path, 'rb') as photo:
                await query.message.reply_photo(
                    photo=photo,
                    caption=text,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
            await query.message.delete()
        else:
            await query.edit_message_text(
                text + "\n\n📷 *Фотография не найдена*",
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
    else:
        await query.edit_message_text("Данные о враче не найдены.")

# Обработчик выбора "Процедуры" внутри "Услуг"
async def button_service_procedures(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = data['procedures']['title']
    keyboard = service_procedures_keyboard()
    await query.edit_message_text(text, reply_markup=keyboard)

# Обработчик выбора процедуры
async def button_procedure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    procedure_key = query.data.replace('procedure_', '')
    procedure_data = data['procedures']['procedures_list'][procedure_key]
    text = f"Процедура: {procedure_data['name']}"
    keyboard = procedure_detail_keyboard(procedure_key)
    await query.edit_message_text(text, reply_markup=keyboard)

# Обработчик выбора направления
async def button_direction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    direction_key = query.data.replace('direction_', '')
    direction_data = data['directions']['directions_list'][direction_key]
    text = f"Направление: {direction_data['name']}"
    keyboard = direction_detail_keyboard(direction_key)
    await query.edit_message_text(text, reply_markup=keyboard)

# Обработчик кнопки "Подробнее" у направления
async def button_direction_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    direction_key = query.data.replace('detail_direction_', '')
    direction_data = data['directions']['directions_list'][direction_key]
    text = f"*{direction_data['name']}*\n\n{direction_data['description']}"
    keyboard = direction_description_keyboard(direction_key)
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')

# Обработчик для кнопки "Подробнее" в описании направления
async def button_direction_more_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    direction_key = query.data.replace('more_detail_direction_', '')
    direction_data = data['directions']['directions_list'][direction_key]
    text = f"*{direction_data['name']}*\n\n{direction_data['detailed_description']}"
    keyboard = direction_detailed_description_keyboard(direction_key)
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')

# Обработчик кнопки "Назад"
async def button_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    back_to = query.data.replace('back_', '')

    try:
        if back_to == 'main_menu':
            text = data['start_message']
            reply_keyboard = main_menu_keyboard()
            await query.message.delete()
            await query.message.reply_text(text, reply_markup=reply_keyboard)

        elif back_to == 'specialists':
            text = data['specialists']['title']
            keyboard = specialists_keyboard()
            await query.message.delete()
            await query.message.reply_text(text, reply_markup=keyboard)

        elif back_to == 'services':
            text = data['services']['title']
            keyboard = services_keyboard()
            await query.edit_message_text(text, reply_markup=keyboard)

        elif back_to == 'service_specialists':
            text = "Выберите специализацию:"
            keyboard = service_specializations_keyboard()
            await query.edit_message_text(text, reply_markup=keyboard)

        elif back_to == 'directions':
            text = data['directions']['title']
            keyboard = directions_keyboard()
            await query.edit_message_text(text, reply_markup=keyboard)

        elif back_to == 'service_specializations':
            text = "Выберите специализацию:"
            keyboard = service_specializations_keyboard()
            await query.edit_message_text(text, reply_markup=keyboard)

        elif back_to == 'service_procedures':
            text = data['procedures']['title']
            keyboard = service_procedures_keyboard()
            await query.edit_message_text(text, reply_markup=keyboard)

        elif back_to.startswith('service_specialization_'):
            specialization_key = back_to.replace('service_specialization_', '')
            if specialization_key in data['specializations']:
                specialization_data = data['specializations'][specialization_key]
                text = f"Выберите врача ({specialization_data['title']}):"
                keyboard = service_specialists_keyboard(specialization_key)
                await query.edit_message_text(text, reply_markup=keyboard)
            else:
                await handle_invalid_state(query, "Специализация не найдена")

        elif back_to == 'appointment':
            await handle_back_from_appointment(update, context)

        else:
            await handle_invalid_state(query, f"Неизвестный пункт возврата: {back_to}")

    except Exception as e:
        logger.error(f"Ошибка в обработчике возврата: {e}")
        await handle_invalid_state(query, "Произошла ошибка при возврате")

# Обработчик для всех кнопок "Записаться"
async def button_appointment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    appointment_data = query.data

    # Разделяем callback_data корректно
    parts = appointment_data.split('_')
    if len(parts) < 2 or parts[0] != 'appointment':
        await query.edit_message_text("Ошибка: неверный формат данных записи")
        return

    appointment_type = parts[1]
    appointment_id = '_'.join(parts[2:])

    # Сохраняем данные для возврата
    context.user_data['appointment_type'] = appointment_type
    context.user_data['appointment_id'] = appointment_id

    # Для врачей из специализаций сохраняем контекст
    if appointment_type == 'doctor':
        context.user_data['is_from_specialization'] = True
    elif appointment_type == 'service_doctor':
        context.user_data['is_from_specialization'] = True
        appointment_type = 'doctor'  # Нормализуем тип
    else:
        context.user_data['is_from_specialization'] = False

    text = "Выберите удобный день для записи:"
    keyboard = appointment_days_keyboard()

    await query.edit_message_text(text, reply_markup=keyboard)
    return DAY

async def select_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    selected_day = query.data.replace('day_', '')
    context.user_data['selected_day'] = selected_day

    await query.edit_message_text("Отлично! Теперь введите ваше имя:")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    context.user_data['name'] = name

    await update.message.reply_text("Спасибо! Теперь введите ваш номер телефона:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    context.user_data['phone'] = phone

    # Получаем данные для подтверждения
    selected_day = context.user_data['selected_day']
    name = context.user_data['name']

    # Формируем подтверждение пользователю
    confirmation_message = data['appointment']['confirmation_message']
    await update.message.reply_text(confirmation_message)

    # Очищаем данные пользователя
    context.user_data.clear()

    # Возвращаем в главное меню
    await main_menu_handler(update, context)
    return ConversationHandler.END

def get_service_or_doctor_name(appointment_type: str, appointment_id: str) -> str:
    """Получает название услуги/врача по типу и ID"""
    try:
        if appointment_type == 'doctor':
            # Сначала ищем в основных специалистах
            if appointment_id in data['specialists']['doctors']:
                doctor_data = data['specialists']['doctors'][appointment_id]
                return f"{doctor_data['name']} ({doctor_data['specialization']})"
            # Затем в специализациях
            for spec_key, specialization in data['specializations'].items():
                if appointment_id in specialization['doctors']:
                    doctor_data = specialization['doctors'][appointment_id]
                    return f"{doctor_data['name']} ({doctor_data['specialization']})"

        elif appointment_type == 'procedure':
            procedure_data = data['procedures']['procedures_list'].get(appointment_id)
            if procedure_data:
                return procedure_data['name']

        elif appointment_type == 'direction':
            direction_data = data['directions']['directions_list'].get(appointment_id)
            if direction_data:
                return direction_data['name']

    except Exception as e:
        logger.error(f"Ошибка получения названия услуги/врача: {e}")
    return "Неизвестная услуга"

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет пользователя в главное меню"""
    welcome_text = data['start_message']
    keyboard = main_menu_keyboard()
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=keyboard)
    else:
        query = update.callback_query
        await query.edit_message_text(welcome_text, reply_markup=keyboard)

async def handle_back_from_appointment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает возврат из процесса записи на приём"""
    query = update.callback_query
    await query.answer()

    appointment_type = context.user_data.get('appointment_type')
    appointment_id = context.user_data.get('appointment_id')

    if not appointment_type or not appointment_id:
        await query.edit_message_text("Данные о записи не найдены. Возврат в главное меню.")
        await main_menu_handler(update, context)
        return

    try:
        if appointment_type == 'doctor':
            is_from_specialization = context.user_data.get('is_from_specialization', False)

            # Ищем врача в зависимости от источника
            if appointment_id in data['specialists']['doctors']:
                doctor_data = data['specialists']['doctors'][appointment_id]
                photo_path = doctor_data.get('photo')
                text = f"*{doctor_data['name']}*\nСпециализация: {doctor_data['specialization']}"
                keyboard = doctor_detail_keyboard(appointment_id)
            elif is_from_specialization:
                # Ищем в специализациях
                doctor_data = None
                for specialization in data['specializations'].values():
                    if appointment_id in specialization['doctors']:
                        doctor_data = specialization['doctors'][appointment_id]
                        break

                if not doctor_data:
                    await query.edit_message_text("Врач не найден. Возврат в главное меню.")
                    await main_menu_handler(update, context)
                    return

                photo_path = doctor_data.get('photo')
                text = f"*{doctor_data['name']}*\nСпециализация: {doctor_data['specialization']}"
                keyboard = service_doctor_detail_keyboard(appointment_id)
            else:
                await query.edit_message_text("Врач не найден. Возврат в главное меню.")
                await main_menu_handler(update, context)
                return

            if photo_path and os.path.exists(photo_path):
                with open(photo_path, 'rb') as photo:
                    await query.message.reply_photo(
                        photo=photo,
                        caption=text,
                        reply_markup=keyboard,
                        parse_mode='Markdown'
                    )
                await query.message.delete()
            else:
                await query.edit_message_text(
                    text + "\n\n📷 *Фотография не найдена*",
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )

        elif appointment_type == 'procedure':
            procedure_data = data['procedures']['procedures_list'].get(appointment_id)
            if not procedure_data:
                await query.edit_message_text("Процедура не найдена. Возврат в главное меню.")
                await main_menu_handler(update, context)
                return

            text = f"Процедура: {procedure_data['name']}"
            keyboard = procedure_detail_keyboard(appointment_id)
            await query.edit_message_text(text, reply_markup=keyboard)

        elif appointment_type == 'direction':
            direction_data = data['directions']['directions_list'].get(appointment_id)
            if not direction_data:
                await query.edit_message_text("Направление не найдено. Возврат в главное меню.")
                await main_menu_handler(update, context)
                return

            text = f"Направление: {direction_data['name']}"
            keyboard = direction_detail_keyboard(appointment_id)
            await query.edit_message_text(text, reply_markup=keyboard)

        else:
            await query.edit_message_text("Неизвестный тип записи. Возврат в главное меню.")
            await main_menu_handler(update, context)

    except Exception as e:
        logger.error(f"Ошибка при возврате из записи: {e}")
        await query.edit_message_text(f"Ошибка: {str(e)}. Возврат в главное меню.")
        await main_menu_handler(update, context)


async def handle_invalid_state(query: Update.callback_query, error_message: str):
    """Обрабатывает некорректные состояния и ошибки"""
    logger.warning(f"Некорректное состояние возврата: {error_message}")
    try:
        await query.edit_message_text(
            f"⚠️ {error_message}\n\nВозврат в главное меню...",
            reply_markup=main_menu_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            # Если сообщение не изменилось, просто возвращаемся в главное меню
            await main_menu_handler(query, None)
        elif "message to edit not found" in str(e):
            # Если сообщение не найдено, отправляем новое
            await query.message.reply_text(
                f"⚠️ {error_message}\n\nВозврат в главное меню...",
                reply_markup=main_menu_keyboard()
            )
        else:
            raise e

async def cancel_appointment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отменяет процесс записи"""
    if update.message:
        await update.message.reply_text(
            "Запись отменена. Выберите другой раздел:",
            reply_markup=main_menu_keyboard()
        )
    elif update.callback_query:
        await update.callback_query.answer("Запись отменена")
        await update.callback_query.edit_message_text(
            "Запись отменена. Выберите другой раздел:",
            reply_markup=main_menu_keyboard()
        )

    context.user_data.clear()
    return ConversationHandler.END