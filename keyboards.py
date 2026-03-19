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
        button = InlineKeyboardButton(f"{doctor['name']} - {doctor['specialization']}",
                                     callback_data=f"doctor_{key}")
        keyboard.append([button])
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_main_menu")])
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для врача (Записаться, Подробнее и Назад) - для главного меню
def doctor_detail_keyboard(doctor_key):
    keyboard = [
        [InlineKeyboardButton("📅 Записаться", callback_data=f"appointment_doctor_{doctor_key}")],
        [InlineKeyboardButton("◀️ Назад", callback_data="back_specialists")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура с описанием врача (Записаться и Назад) - для главного меню
def doctor_description_keyboard(doctor_key):
    keyboard = [
        [InlineKeyboardButton("📅 Записаться", callback_data=f"appointment_doctor_{doctor_key}")],
        [InlineKeyboardButton("◀️ Назад", callback_data="back_specialists")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для меню "Услуги"
def services_keyboard():
    keyboard = []
    for button_text in data['services']['buttons']:
        callback_data = "service_specialists" if button_text == "Специалисты" else "service_procedures"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_main_menu")])
    return InlineKeyboardMarkup(keyboard)

# Клавиатура со списком специализаций (из услуг)
def service_specializations_keyboard():
    keyboard = []
    for key, specialization in data['specializations'].items():
        button = InlineKeyboardButton(f"{specialization['title']}", callback_data=f"specialization_{key}")
        keyboard.append([button])
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_services")])
    return InlineKeyboardMarkup(keyboard)

# Клавиатура со списком врачей специализации (из услуг)
def service_specialists_keyboard(specialization_key):
    keyboard = []
    specialization = data['specializations'][specialization_key]
    for key, doctor in specialization['doctors'].items():
        button = InlineKeyboardButton(f"{doctor['name']}", callback_data=f"service_doctor_{key}")
        keyboard.append([button])
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_service_specializations")])
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для врача из услуг (Записаться, Подробнее и Назад)
def service_doctor_detail_keyboard(doctor_key):
    keyboard = [
        [
            InlineKeyboardButton("📅 Записаться", callback_data=f"appointment_service_doctor_{doctor_key}"),
            InlineKeyboardButton("📖 Подробнее", callback_data=f"detail_service_doctor_{doctor_key}")
        ],
        [InlineKeyboardButton("◀️ Назад", callback_data=f"back_service_doctors_{doctor_key}")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура с описанием врача из услуг (Записаться и Назад)
def service_doctor_description_keyboard(doctor_key):
    keyboard = [
        [InlineKeyboardButton("📅 Записаться", callback_data=f"appointment_service_doctor_{doctor_key}")],
        [InlineKeyboardButton("◀️ Назад", callback_data=f"back_service_doctor_{doctor_key}")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура со списком процедур (из услуг)
def service_procedures_keyboard():
    keyboard = []
    for key, procedure in data['procedures']['procedures_list'].items():
        button = InlineKeyboardButton(f"{procedure['name']}", callback_data=f"procedure_{key}")
        keyboard.append([button])
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_services")])
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для процедуры (Записаться и Назад)
def procedure_detail_keyboard(procedure_key):
    keyboard = [
        [InlineKeyboardButton("📅 Записаться", callback_data=f"appointment_procedure_{procedure_key}")],
        [InlineKeyboardButton("◀️ Назад", callback_data="back_service_procedures")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура со списком направлений
def directions_keyboard():
    keyboard = []
    for key, direction in data['directions']['directions_list'].items():
        button = InlineKeyboardButton(f"{direction['name']}", callback_data=f"direction_{key}")
        keyboard.append([button])
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_main_menu")])
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для направления (Подробнее, Записаться и Назад)
def direction_detail_keyboard(direction_key):
    keyboard = [
        [
            InlineKeyboardButton("📖 Подробнее", callback_data=f"detail_direction_{direction_key}"),
            InlineKeyboardButton("📅 Записаться", callback_data=f"appointment_direction_{direction_key}")
        ],
        [InlineKeyboardButton("◀️ Назад", callback_data="back_directions")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для описания направления (Записаться и Назад)
def direction_description_keyboard(direction_key):
    keyboard = [
        [
            InlineKeyboardButton("📖 Подробнее", callback_data=f"more_detail_direction_{direction_key}"),
            InlineKeyboardButton("📅 Записаться", callback_data=f"appointment_direction_{direction_key}")
        ],
        [InlineKeyboardButton("◀️ Назад", callback_data="back_directions")]
    ]
    return InlineKeyboardMarkup(keyboard)

def direction_detailed_description_keyboard(direction_key):
    keyboard = [
        [InlineKeyboardButton("📅 Записаться", callback_data=f"appointment_direction_{direction_key}")],
        [InlineKeyboardButton("◀️ Назад", callback_data=f"back_direction_{direction_key}")]
    ]
    return InlineKeyboardMarkup(keyboard)