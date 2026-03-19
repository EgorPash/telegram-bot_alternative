# Файл, генерирующий клавиатуры
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import json

# Загружаем данные из JSON
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# --- Главное меню (Reply клавиатура) ---
def main_menu_keyboard():
    buttons = [KeyboardButton(text) for text in data['main_menu']['buttons']]
    keyboard = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, input_field_placeholder="Выберите опцию")

# --- Inline клавиатуры ---

# Клавиатура со списком специалистов (из главного меню)
def specialists_keyboard():
    keyboard = []
    for key, doctor in data['specialists']['doctors'].items():
        button = InlineKeyboardButton(f"{doctor['name']} - {doctor['specialization']}", callback_data=f"doctor_{key}")
        keyboard.append([button])
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_main_menu")])
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для врача (Записаться, Подробнее и Назад) - для главного меню
def doctor_detail_keyboard(doctor_key):
    keyboard = [
        [InlineKeyboardButton("📅 Записаться", callback_data=f"appointment_doctor_{doctor_key}")],
        [InlineKeyboardButton("📖 Подробнее", callback_data=f"detail_doctor_{doctor_key}")],
        [InlineKeyboardButton("◀️ Назад", callback_data="back_specialists")]  # ✅ Исправлено: back_specialists
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура с описанием врача (Записаться и Назад) - для главного меню
def doctor_description_keyboard(doctor_key):
    keyboard = [
        [InlineKeyboardButton("📅 Записаться", callback_data=f"appointment_doctor_{doctor_key}")],
        [InlineKeyboardButton("◀️ Назад", callback_data="back_specialists")]  # ✅ Исправлено: back_specialists
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура специализаций в разделе "Услуги"
def service_specializations_keyboard():
    keyboard = []
    for spec_key, spec_data in data['specializations'].items():
        button = InlineKeyboardButton(spec_data['title'], callback_data=f"specialization_{spec_key}")
        keyboard.append([button])
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_services")])
    return InlineKeyboardMarkup(keyboard)

# Клавиатура списка врачей по специализации в разделе "Услуги"
def service_specialists_keyboard(specialization_key):
    keyboard = []
    for doctor_key, doctor in data['specializations'][specialization_key]['doctors'].items():
        button = InlineKeyboardButton(f"{doctor['name']} - {doctor['specialization']}", callback_data=f"service_doctor_{doctor_key}")
        keyboard.append([button])
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_service_specializations")])
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для карточки врача в разделе "Услуги" (Записаться, Подробнее, Назад)
def service_doctor_detail_keyboard(doctor_key):
    keyboard = [
        [InlineKeyboardButton("📅 Записаться", callback_data=f"appointment_doctor_{doctor_key}")],
        [InlineKeyboardButton("📖 Подробнее", callback_data=f"detail_service_doctor_{doctor_key}")],
        [InlineKeyboardButton("◀️ Назад", callback_data=f"back_service_doctor_{doctor_key}")]  # ✅ ИСПРАВЛЕНО: без 's' — согласовано с handlers.py
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для описания врача в разделе "Услуги" (Записаться, Назад)
def service_doctor_description_keyboard(doctor_key):
    keyboard = [
        [InlineKeyboardButton("📅 Записаться", callback_data=f"appointment_doctor_{doctor_key}")],
        [InlineKeyboardButton("◀️ Назад", callback_data=f"back_service_doctor_{doctor_key}")]  # ✅ ИСПРАВЛЕНО: без 's'
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура списка процедур в разделе "Услуги"
def service_procedures_keyboard():
    keyboard = []
    for proc_key, proc_data in data['procedures']['procedures_list'].items():
        button = InlineKeyboardButton(proc_data['name'], callback_data=f"procedure_{proc_key}")
        keyboard.append([button])
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_services")])
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для деталей процедуры
def procedure_detail_keyboard(procedure_key):
    keyboard = [
        [InlineKeyboardButton("📅 Записаться", callback_data=f"appointment_procedure_{procedure_key}")],
        [InlineKeyboardButton("◀️ Назад", callback_data="back_service_procedures")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура списка направлений
def directions_keyboard():
    keyboard = []
    for dir_key, dir_data in data['directions']['directions_list'].items():
        button = InlineKeyboardButton(dir_data['name'], callback_data=f"direction_{dir_key}")
        keyboard.append([button])
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_main_menu")])
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для деталей направления
def direction_detail_keyboard(direction_key):
    keyboard = [
        [InlineKeyboardButton("📖 Подробнее", callback_data=f"detail_direction_{direction_key}")],
        [InlineKeyboardButton("◀️ Назад", callback_data="back_directions")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для описания направления
def direction_description_keyboard(direction_key):
    keyboard = [
        [InlineKeyboardButton("📖 Подробнее", callback_data=f"more_detail_direction_{direction_key}")],
        [InlineKeyboardButton("◀️ Назад", callback_data=f"direction_{direction_key}")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для подробного описания направления
def direction_detailed_description_keyboard(direction_key):
    keyboard = [
        [InlineKeyboardButton("◀️ Назад", callback_data=f"detail_direction_{direction_key}")]
    ]
    return InlineKeyboardMarkup(keyboard)
