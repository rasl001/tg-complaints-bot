# Telegram Complaints Bot 🤖

## 🌟 English

A Python-based Telegram bot designed for handling user complaints, built with **aiogram 3.x** and **SQLite**. 
This bot allows users to submit complaints, which are assigned unique IDs, and provides an admin panel for managing welcome messages, info text, and viewing complaints.

### 🚀 Features
- **Complaint Submission**: Users can submit complaints, receiving a confirmation with a unique complaint ID. Admins are notified instantly.
- **Dynamic Menus**: Main menu with "Home", "Info", and "Submit Complaint" buttons. Admins see an additional "Admin Panel" button.
- **Admin Panel**:
  - Edit welcome message and info text, stored in SQLite.
  - View a list of new complaints with their IDs and usernames.
  - Return to the main menu after editing with success confirmation.
- **Database**: SQLite stores complaints (ID, user ID, username, text, status) and settings (welcome/info texts).
- **Secure Admin Access**: Admin features are restricted to a specific ADMIN_ID.

### 🛠️ Installation
1. Install the required package:
   ```bash
   pip install aiogram
   ```
2. Update `BOT_TOKEN` and `ADMIN_ID` in `bot.py` with your values.
3. Run the bot:
   ```bash
   python bot.py
   ```

### 📜 License
MIT License

---

## 🌟 Русский

Бот для Telegram на Python, предназначенный для приема жалоб от пользователей, построенный на **aiogram 3.x** и **SQLite**. 
Этот бот позволяет пользователям отправлять жалобы, которым присваиваются уникальные номера, и предоставляет админ-панель для управления текстами приветствия, информацией и просмотра жалоб.

### 🚀 Возможности
- **Подача жалоб**: Пользователи могут отправлять жалобы, получая подтверждение с уникальным номером. Админ уведомляется сразу.
- **Динамические меню**: Главное меню с кнопками "Главная", "Информация" и "Подать жалобу". Для админа добавляется кнопка "Админка".
- **Админ-панель**:
  - Редактирование приветственного сообщения и текста информации, сохраняемых в SQLite.
  - Просмотр списка новых жалоб с номерами и именами пользователей.
  - Возврат в главное меню после редактирования с подтверждением успеха.
- **База данных**: SQLite хранит жалобы (ID, ID пользователя, имя пользователя, текст, статус) и настройки (тексты приветствия и информации).
- **Безопасный доступ админа**: Функции админки доступны только для заданного ADMIN_ID.

### 🛠️ Установка
1. Установите необходимую библиотеку:
   ```bash
   pip install aiogram
   ```
2. Обновите `BOT_TOKEN` и `ADMIN_ID` в файле `bot.py` своими значениями.
3. Запустите бота:
   ```bash
   python bot.py
   ```

### 📜 Лицензия
Лицензия MIT
