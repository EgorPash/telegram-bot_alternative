# Файл с обработчками команд и сообщений
from telegram import Update
from telegram.ext import ContextTypes
import json
from keyboards import *

# Загружаем данные из JSON
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = data['start_message']
    keyboard = main_menu_keyboard()
    await update.message.reply_text(welcome_text, reply_markup=keyboard)


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

    text = f"*{doctor_data['name']}*\nСпециализация: {doctor_data['specialization']}"
    keyboard = doctor_detail_keyboard(doctor_key)
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')


# Обработчик кнопки "Подробнее" о враче (главное меню)
async def button_doctor_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    doctor_key = query.data.replace('detail_doctor_', '')
    doctor_data = data['specialists']['doctors'][doctor_key]

    text = f"*{doctor_data['name']}*\nСпециализация: {doctor_data['specialization']}\n\n{doctor_data['description']}"
    keyboard = doctor_description_keyboard(doctor_key)
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')


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

    # Получаем ключ врача
    doctor_key = query.data.replace('service_doctor_', '')

    # Ищем врача во всех специализациях
    doctor_data = None
    for specialization in data['specializations'].values():
        if doctor_key in specialization['doctors']:
            doctor_data = specialization['doctors'][doctor_key]
            break

    if doctor_data:
        text = f"*{doctor_data['name']}*\nСпециализация: {doctor_data['specialization']}"
        keyboard = service_doctor_detail_keyboard(doctor_key)
        await query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')
    else:
        await query.edit_message_text("Данные о враче не найдены.")


# Обработчик кнопки "Подробнее" о враче из услуг
async def button_service_doctor_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Получаем ключ врача
    doctor_key = query.data.replace('detail_service_doctor_', '')

    # Ищем врача во всех специализациях
    doctor_data = None
    for specialization in data['specializations'].values():
        if doctor_key in specialization['doctors']:
            doctor_data = specialization['doctors'][doctor_key]
            break

    if doctor_data:
        text = f"*{doctor_data['name']}*\nСпециализация: {doctor_data['specialization']}\n\n{doctor_data['description']}"
        keyboard = service_doctor_description_keyboard(doctor_key)
        await query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')
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


# Обработчик кнопки "Назад"
async def button_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    back_to = query.data.replace('back_', '')

    if back_to == 'main_menu':
        text = data['start_message']
        # Для главного меню используем reply-клавиатуру, а не inline
        reply_keyboard = main_menu_keyboard()
        await query.message.reply_text(text, reply_markup=reply_keyboard)
        await query.delete_message()

    elif back_to == 'specialists':
        text = data['specialists']['title']
        keyboard = specialists_keyboard()
        await query.edit_message_text(text, reply_markup=keyboard)

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

    elif back_to == 'service_specialization':
        # Этот вариант нужно уточнить в зависимости от контекста
        text = "Выберите специализацию:"
        keyboard = service_specializations_keyboard()
        await query.edit_message_text(text, reply_markup=keyboard)

    elif back_to == 'service_procedures':
        text = data['procedures']['title']
        keyboard = service_procedures_keyboard()
        await query.edit_message_text(text, reply_markup=keyboard)


# Общий обработчик для всех кнопок "Записаться"
async def button_appointment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    appointment_data = query.data.replace('appointment_', '')
    await query.message.reply_text("Функция записи будет реализована позже")
