# Файл с обработчиками команд и сообщений
import logging
import os
from telegram import Update
from telegram.ext import ContextTypes
import json
from keyboards import *

logger = logging.getLogger(__name__)

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
    specialization_data = data['specializations'][specialization_key]
    text = f"Выберите врача ({specialization_data['title']}):"
    keyboard = service_specialists_keyboard(specialization_key)
    await query.edit_message_text(text, reply_markup=keyboard)

# Обработчик выбора врача из услуг
async def button_service_doctor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    doctor_key = query.data.replace('service_doctor_', '')
    doctor_data = None
    for specialization in data['specializations'].values():
        if doctor_key in specialization['doctors']:
            doctor_data = specialization['doctors'][doctor_key]
            break
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
    doctor_data = None
    for specialization in data['specializations'].values():
        if doctor_key in specialization['doctors']:
            doctor_data = specialization['doctors'][doctor_key]
            break
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

    if back_to == 'main_menu':
        text = data['start_message']
        reply_keyboard = main_menu_keyboard()
        await query.message.reply_text(text, reply_markup=reply_keyboard)
        await query.message.delete()

    elif back_to == 'specialists':
        # Возвращаемся к списку врачей
        text = data['specialists']['title']
        keyboard = specialists_keyboard()
        await query.edit_message_text(text, reply_markup=keyboard)

    elif back_to.startswith('specialization_'):
        # Возврат к списку врачей специализации
        specialization_key = back_to.replace('specialization_', '')
        if specialization_key in data['specializations']:
            specialization_data = data['specializations'][specialization_key]
            text = f"Выберите врача ({specialization_data['title']}):"
            keyboard = service_specialists_keyboard(specialization_key)
            await query.edit_message_text(text, reply_markup=keyboard)
        else:
            await query.edit_message_text("Специализация не найдена.")

    elif back_to == 'services':
        text = data['services']['title']
        keyboard = services_keyboard()
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

    # Возврат из карточки врача в разделе "Специалисты"
    elif back_to == 'doctor_list':
        text = data['specialists']['title']
        keyboard = specialists_keyboard()
        await query.edit_message_text(text, reply_markup=keyboard)

    # Возврат из карточки врача в разделе "Услуги" → "Специалисты" → специализация
    elif back_to.startswith('service_specialization_'):
        specialization_key = back_to.replace('service_specialization_', '')
        if specialization_key in data['specializations']:
            specialization_data = data['specializations'][specialization_key]
            text = f"Выберите врача ({specialization_data['title']}):"
            keyboard = service_specialists_keyboard(specialization_key)
            await query.edit_message_text(text, reply_markup=keyboard)
        else:
            await query.edit_message_text("Специализация не найдена.")

    else:
        await query.edit_message_text("Неизвестная команда возврата.")


# Общий обработчик для всех кнопок "Записаться"
async def button_appointment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    appointment_data = query.data.replace('appointment_', '')
    await query.message.reply_text("Функция записи будет реализована позже")
