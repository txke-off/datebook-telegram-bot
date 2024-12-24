from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F
from aiogram.utils.token import TokenValidationError
import sqlite3
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv("a/api_token.env")
API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

conn = sqlite3.connect('daily_tasks.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
date TEXT NOT NULL,
time TEXT NOT NULL,
description TEXT,
UNIQUE(user_id, date, time)
)
""")
conn.commit()

@router.message(F.text.startswith("/start"))
async def start_command(message: Message):
    await message.reply(
        "Привет! Я бот для управления задачами. Вот что я умею:\n\n"
        "📌 Команды:\n"
        "/add YYYY-MM-DD HH:MM описание - добавить задачу\n"
        "/delete YYYY-MM-DD HH:MM - удалить задачу\n"
        "/show - показать задачи на неделю\n"
        "/help - помощь\n\n"
    )

@router.message(F.text.startswith("/add"))
async def add_task(message: Message):
    try:
        _, date, time, description = message.text.split(maxsplit=3)
        try:
            datetime.strptime(date, "%Y-%m-%d")
            datetime.strptime(time, "%H:%M")
        except ValueError:
            raise ValueError("Неверный формат даты или времени.")
        user_id = message.from_user.id
        cursor.execute("INSERT INTO tasks (user_id, date, time, description) VALUES (?, ?, ?, ?)", (user_id, date, time, description))
        conn.commit()
        await message.reply(f"Добавлена задача на {date} {time}: {description}")
    except sqlite3.IntegrityError:
        await message.reply(f"На {date} {time} уже есть задача. Удалите её перед добавлением новой.")
    except ValueError:
        await message.reply("Используйте формат: /add YYYY-MM-DD HH:MM описание")

@router.message(F.text.startswith("/delete"))
async def delete_task(message: Message):
    try:
        _, date, time = message.text.split(maxsplit=2)
        user_id = message.from_user.id
        cursor.execute("DELETE FROM tasks WHERE user_id = ? AND date = ? AND time = ?", (user_id, date, time))
        if cursor.rowcount > 0:
            conn.commit()
            await message.reply(f"Задача на {date} {time} удалена.")
        else:
            await message.reply(f"Задачи на {date} {time} не существует.")
    except ValueError:
        await message.reply("Используйте формат: /delete YYYY-MM-DD HH:MM")

@router.message(F.text.startswith("/show"))
async def show_tasks(message: Message):
    try:
        args = message.text.split()
        user_id = message.from_user.id

        days_forward = int(args[1]) if len(args) > 1 else 7
        if days_forward <= 0:
            raise ValueError("Диапазон должен быть положительным числом.")
        today = datetime.now().date()
        end_date = today + timedelta(days=days_forward)

        cursor.execute("""
        SELECT date, time, description FROM tasks
        WHERE user_id = ? AND date BETWEEN ? AND ?
        ORDER BY date, time
        """, (user_id, today, end_date))
        tasks = cursor.fetchall()

        if tasks:
            grouped_tasks = {}
            for date, time, desc in tasks:
                if date not in grouped_tasks:
                    grouped_tasks[date] = []
                grouped_tasks[date].append(f"{time} - {desc}")
            text = f"Ваши задачи на ближайшие {days_forward} дней:\n"
            days_ru = {
                    "Monday": "Понедельник", "Tuesday": "Вторник", "Wednesday": "Среда",
                    "Thursday": "Четверг", "Friday": "Пятница", "Saturday": "Суббота",
                    "Sunday": "Воскресенье"
                }
            for date, task_list in grouped_tasks.items():
                day_of_week = days_ru[datetime.strptime(date, "%Y-%m-%d").strftime("%A")]
                date_header = f"📅 {date} ({day_of_week}):\n"
                tasks_for_date = "\n".join(task_list)
                text += f"{date_header}{tasks_for_date}\n\n"
            await message.reply(text.strip())
        else:
            await message.reply(f"На ближайшие {days_forward} дней задач нет.")
    except ValueError:
        await message.reply("Используйте формат: /show [количество дней], где количество дней - положительное число.")

@router.message(F.text.startswith("/help"))
async def show_help(message: Message):
    await message.reply(
        "Команды:\n"
        "/add YYYY-MM-DD HH:MM описание - добавить задачу\n"
        "/delete YYYY-MM-DD HH:MM - удалить задачу\n"
        "/show [количество дней] - показать задачи на указанное количество дней\n"
        "/help - помощь"
    )

dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except TokenValidationError:
        print("Убедитесь, что токен бота корректен.")