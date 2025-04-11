import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Конфигурация
TOKEN = 'TOKEN'
ADMIN_ID = 000000000

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


# Состояния FSM
class UserState(StatesGroup):
    waiting_for_complaint = State()
    waiting_for_welcome = State()
    waiting_for_info = State()


# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS complaints 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  username TEXT, 
                  text TEXT, 
                  status TEXT DEFAULT 'new')''')
    c.execute('''CREATE TABLE IF NOT EXISTS settings 
                 (key TEXT PRIMARY KEY, 
                  value TEXT)''')
    # Установка значений по умолчанию
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('welcome', 'Добро пожаловать в бот жалоб!')")
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('info', 'Здесь будет информация')")
    conn.commit()
    conn.close()


# Главное меню
def get_main_menu(is_admin=False):
    keyboard = [
        [KeyboardButton(text="Главная"), KeyboardButton(text="Информация")],
        [KeyboardButton(text="Подать жалобу")]
    ]
    if is_admin:
        keyboard.append([KeyboardButton(text="Админка")])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


# Админское меню
def get_admin_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Редактировать Главная"), KeyboardButton(text="Редактировать Информация")],
            [KeyboardButton(text="Заявки"), KeyboardButton(text="Вернуться в меню")]
        ],
        resize_keyboard=True
    )
    return keyboard


# Стартовая команда
@router.message(Command("start"))
async def start_command(message: types.Message):
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key='welcome'")
    welcome_text = c.fetchone()[0]
    conn.close()

    is_admin = message.from_user.id == ADMIN_ID
    await message.answer(welcome_text, reply_markup=get_main_menu(is_admin))


# Обработка кнопок меню
@router.message(lambda message: message.text in ["Главная", "Информация", "Подать жалобу", "Админка"])
async def handle_menu(message: types.Message, state: FSMContext):
    is_admin = message.from_user.id == ADMIN_ID

    if message.text == "Главная":
        conn = sqlite3.connect('complaints.db')
        c = conn.cursor()
        c.execute("SELECT value FROM settings WHERE key='welcome'")
        welcome_text = c.fetchone()[0]
        conn.close()
        await message.answer(welcome_text, reply_markup=get_main_menu(is_admin))

    elif message.text == "Информация":
        conn = sqlite3.connect('complaints.db')
        c = conn.cursor()
        c.execute("SELECT value FROM settings WHERE key='info'")
        info_text = c.fetchone()[0]
        conn.close()
        await message.answer(info_text, reply_markup=get_main_menu(is_admin))

    elif message.text == "Подать жалобу":
        await message.answer("Пожалуйста, напишите вашу жалобу:", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserState.waiting_for_complaint)

    elif message.text == "Админка" and is_admin:
        await message.answer("Добро пожаловать в админ-панель", reply_markup=get_admin_menu())


# Обработка жалобы
@router.message(StateFilter(UserState.waiting_for_complaint))
async def process_complaint(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute("INSERT INTO complaints (user_id, username, text) VALUES (?, ?, ?)",
              (message.from_user.id, message.from_user.username, message.text))
    complaint_id = c.lastrowid
    conn.commit()
    conn.close()

    is_admin = message.from_user.id == ADMIN_ID
    await message.answer(f"Ваша заявка №{complaint_id} принята. С Вами свяжется менеджер.",
                         reply_markup=get_main_menu(is_admin))

    # Уведомление админа
    await bot.send_message(
        ADMIN_ID,
        f"Новая жалоба №{complaint_id}\nОт: @{message.from_user.username}\nТекст: {message.text}"
    )

    await state.clear()


# Обработка админских команд
@router.message(lambda message: message.from_user.id == ADMIN_ID and
                                message.text in ["Редактировать Главная", "Редактировать Информация", "Заявки",
                                                 "Вернуться в меню"])
async def handle_admin(message: types.Message, state: FSMContext):
    is_admin = True

    if message.text == "Редактировать Главная":
        await message.answer("Введите новый текст приветствия:", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserState.waiting_for_welcome)

    elif message.text == "Редактировать Информация":
        await message.answer("Введите новый текст информации:", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserState.waiting_for_info)

    elif message.text == "Заявки":
        conn = sqlite3.connect('complaints.db')
        c = conn.cursor()
        c.execute("SELECT id, username FROM complaints WHERE status='new'")
        complaints = c.fetchall()
        conn.close()

        if not complaints:
            await message.answer("Новых заявок нет", reply_markup=get_admin_menu())
        else:
            text = "Список заявок:\n"
            for complaint in complaints:
                text += f"№{complaint[0]} от @{complaint[1]}\n"
            await message.answer(text, reply_markup=get_admin_menu())

    elif message.text == "Вернуться в меню":
        conn = sqlite3.connect('complaints.db')
        c = conn.cursor()
        c.execute("SELECT value FROM settings WHERE key='welcome'")
        welcome_text = c.fetchone()[0]
        conn.close()
        await message.answer(welcome_text, reply_markup=get_main_menu(is_admin))


# Обработка редактирования текстов для админа
@router.message(StateFilter(UserState.waiting_for_welcome), lambda message: message.from_user.id == ADMIN_ID)
async def update_welcome(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute("UPDATE settings SET value=? WHERE key='welcome'", (message.text,))
    conn.commit()
    conn.close()

    await message.answer("Текст приветствия успешно обновлен", reply_markup=get_main_menu(True))
    await state.clear()


@router.message(StateFilter(UserState.waiting_for_info), lambda message: message.from_user.id == ADMIN_ID)
async def update_info(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute("UPDATE settings SET value=? WHERE key='info'", (message.text,))
    conn.commit()
    conn.close()

    await message.answer("Текст информации успешно обновлен", reply_markup=get_main_menu(True))
    await state.clear()


# Запуск бота
async def main():
    init_db()
    print("БОТ ЗАПУЩЕН")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())