
# Telegram Expense Tracker Bot

This is a Telegram bot for managing personal expenses and income. The bot allows users to record transactions, view statistics, and export data to Excel.

---

## Features

- **Add Transactions**: Record income and expenses by sending messages in the format:  
  `<amount> <category>`  
  Positive amounts represent income, and negative amounts represent expenses.

- **Statistics**: View overall statistics and breakdowns by category or month.

- **Export to Excel**: Generate an Excel file with all recorded transactions.

---

## Setup and Installation

### Prerequisites

- Python 3.9 or later
- Telegram Bot Token (get one from [BotFather](https://core.telegram.org/bots#botfather))

### Installation Steps

1. **Clone this repository**:
    ```bash
    git clone https://github.com/jkulds/jkulds_tg_cashee_bot.git
    cd expense-tracker-bot
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:  
    Set the `API_KEY` environment variable with your Telegram bot token.  
    For example, on Linux/macOS:
    ```bash
    export API_KEY="your-telegram-bot-token"
    ```

4. **Run the bot**:
    ```bash
    python bot.py
    ```

---

## Usage

### Commands

- `/start`: Initialize the bot and access the main menu.

### Actions via Buttons

- **Statistics**: Displays the total balance and breakdown of expenses/income by category.
- **Monthly Statistics**: Shows a month-by-month breakdown of transactions.
- **Export**: Generates and sends an Excel file containing all your transactions.

### Manual Input

- To add a transaction, send a message in the format:  
  `<amount> <category>`  
  Example:  
  - `500 Salary` (Adds 500 as income in the "Salary" category)
  - `-150 Groceries` (Adds 150 as an expense in the "Groceries" category)

---

## File Structure

```
.
├── bot.py              # Main bot script
├── README.md           # Readme file
├── expenses_data.json  # Storage file for user data (auto-generated)
├── requirements.txt    # Python dependencies
└── statistics.xlsx     # Exported Excel file (auto-generated)
```

---

## Dependencies

- `python-telegram-bot`: For Telegram bot interactions
- `pandas`: For data manipulation and export
- `xlsxwriter`: For Excel file generation

Install all dependencies with:
```bash
pip install -r requirements.txt
```

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
