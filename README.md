# Datebook Telegram Bot

This is a multi-user task manager bot for Telegram, designed to help users create, manage, and view tasks efficiently.

## Features

- **Add Tasks**: Users can add tasks with specific dates and times.
- **Delete Tasks**: Delete specific tasks or all occurrences of a recurring task.
- **View Tasks**: Display tasks within a custom date range, including day names.
- **Multi-user Support**: Each user’s tasks are stored and managed independently.

## Available Commands

- `/start`: Start the bot and view a welcome message.
- `/add YYYY-MM-DD HH:MM description`: Add a task for a specific date and time.
- `/delete YYYY-MM-DD HH:MM`: Delete a specific task.
- `/show [days]`: Show tasks for the next `days` (default: 7).
- `/help`: View the list of commands and usage instructions.

## Technical Details

- **Programming Language**: Python
- **Database**: SQLite
- **Dependencies**:
  - `aiogram` for Telegram bot interaction.
  - `sqlite3` for task data storage.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/txke-off/datebook-telegram-bot
   cd datebook-telegram-bot
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your bot's API token in the `.env` file:
   ```env
   API_TOKEN=your_telegram_bot_token
   ```
4. Run the bot:
   ```bash
   datebook_bot.py
   ```

## Notes

- Currently, the bot supports only Russian language. English localization is planned in the future.

---

Happy task managing!


