import os
import json
import pandas as pd

from collections import defaultdict
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
)
from datetime import datetime

API_KEY = os.environ['API_KEY']

DATA_FILE = "expenses_data.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as file:
        user_expenses = json.load(file)
else:
    user_expenses = {}

def save_data():
    """Сохранение данных в файл"""
    with open(DATA_FILE, "w") as file:
        json.dump(user_expenses, file, indent=4)

MAIN_MENU = ReplyKeyboardMarkup(
    [["Статистика", "Статистика по месяцам"],["Экспорт"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    await update.message.reply_text(
        "Привет! Я бот для учета расходов. Используйте меню для выбора дейстия.",
        reply_markup=MAIN_MENU
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений и нажатий на кнопки"""
    text = update.message.text

    if text in ["Статистика", "Статистика по месяцам", "Экспорт"]:
        await handle_button_click(update, context, text)
    else:
        await handle_user_input(update, context, text)

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """Обработка нажатий на кнопки"""
    user_id = str(update.effective_user.id)
    if text == "Статистика":
        stats = generate_stats(user_id)
        await update.message.reply_text(stats)
    elif text == "Статистика по месяцам":
        stats = generate_monthly_stats(user_id)
        await update.message.reply_text(stats)
    elif text == "Экспорт":
        await export_statistics(update)

async def handle_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """Обработка произвольного ввода пользователя"""
    user_id = str(update.effective_user.id)
    if user_id not in user_expenses:
        user_expenses[user_id] = []
        save_data()

    try:
        amount, category = text.split(maxsplit=1)
        if (len(category) == 0):
            await update.message.reply_text("Некорректная категория.")
            return
        
        amount = float(amount)
        date = datetime.today().strftime('%d.%m.%Y')
        isExpense = amount < 0
        if isExpense:
            user_expenses[user_id].append({"type": "expense", "amount": -amount, "category": category, "date": date})
        else:
            user_expenses[user_id].append({"type": "income", "amount": amount, "category": category, "date": date})

        message = "расход" if isExpense else "доход"
        await update.message.reply_text(f"Добавлен {message}: {amount} в категории '{category}'", reply_markup=MAIN_MENU)
        save_data()
    except ValueError:
        await update.message.reply_text("Ошибка ввода. Убедитесь, что ввели сумму и категорию через пробел.")

def generate_stats(user_id: str):
    """Генерация статистики для пользователя"""
    expenses = user_expenses.get(user_id, [])
    if not expenses:
        return "Нет данных для отображения."
    
    total_expenses = sum(item["amount"] for item in expenses)
    categories = {}
    for item in expenses:
        categories[item["category"]] = categories.get(item["category"], 0) + item["amount"]
    
    category_stats = "\n".join([f"{cat}: {amt}" for cat, amt in categories.items()])
    return f"Общий баланс: {total_expenses}\nПо категориям:\n{category_stats}"

def generate_monthly_stats(user_id: str):
    """Генерация статистики по месяцам для пользователя"""
    expenses = user_expenses.get(user_id, [])
    if not expenses:
        return "Нет данных для отображения."

    monthly_stats = defaultdict(lambda: defaultdict(float))
    for item in expenses:
        date = datetime.strptime(item["date"], '%d.%m.%Y')
        month_key = date.strftime('%Y.%m')  # Группировка по году и месяцу
        monthly_stats[month_key][item["category"]] += item["amount"]

    report = []
    for month, categories in sorted(monthly_stats.items()):
        report.append(f"\n📅 {month}")
        for category, amount in categories.items():
            report.append(f"  {category}: {amount:.2f}")
    return "\n".join(report)

async def export_statistics(update: Update):
    """Экспорт статистики в Excel"""
    user_id = str(update.effective_user.id)

    df = pd.DataFrame(user_expenses[user_id])
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
    (max_row, max_col) = df.shape
    file_path = 'statistics.xlsx'
    
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter', date_format='dd.mm.yyyy', datetime_format='dd.mm.yyyy')

    df.to_excel(writer, sheet_name="Статистика", index=False)

    ws = writer.sheets['Статистика']
    ws.autofilter(0, 0, max_row, max_col-1)
    ws.autofit()

    writer.close()

    with open(file_path, 'rb') as file:
        await update.message.reply_document(document=file, filename='statistics.xlsx')

async def error_handler(_: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Произошла ошибка: {context.error}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(API_KEY).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    while(True):
        try:
            print("Бот запущен...")
            app.run_polling()
        except Exception as e:
            print(f"Произошла ошибка при запуске бота, {e}")
