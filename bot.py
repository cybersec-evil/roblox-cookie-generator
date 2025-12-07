import random
import string
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "7663042780:AAHUDkUY4Dgfm8Ng51f8BlfvyFDDW_fwVxE"  # сюда токен

# список префиксов 
prefixes = [
    "_CAEaAhAB.293E36D6BFE83F87E45DEA8CE99241563B47A5B072FD6315516",
    "_GgIQAQ.201F5C26943D438CE6C655859F7B4BD8AC"
]

warning = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_"

def generate_cookie():
    # 50% шанс добавить префикс
    use_prefix = random.random() < 0.5

    # рандомная длина hex части
    hex_length = random.randint(800, 1200)
    hex_part = ''.join(random.choices(string.hexdigits.upper(), k=hex_length))

    if use_prefix:
        prefix = random.choice(prefixes)
        return f"{warning}{prefix}{hex_part}"
    else:
        return f"{warning}{hex_part}"

# меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("10 кук", callback_data="10"),
         InlineKeyboardButton("100 кук", callback_data="100")],
        [InlineKeyboardButton("1000 кук", callback_data="1000"),
         InlineKeyboardButton("Введите своё число", callback_data="custom")]
    ]
    await update.message.reply_text(
        "выбери сколько сгенерировать или введи своё кол-во:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id

    if query.data == "custom":
        context.user_data["awaiting"] = True
        await query.message.reply_text("📝 введи количество кук (например 50):")
    else:
        count = int(query.data)
        await generate_and_send(chat_id, count, context)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if context.user_data.get("awaiting"):
        try:
            count = int(update.message.text)
            if count <= 0 or count > 100_000:
                await update.message.reply_text("❗ число должно быть от 1 до 100000")
                return
            context.user_data["awaiting"] = False
            await generate_and_send(chat_id, count, context)
        except:
            await update.message.reply_text("❗ введи целое число")

async def generate_and_send(chat_id, count, context):
    await context.bot.send_message(chat_id, text=f"🚀 генерация {count} кук...")

    cookies = [generate_cookie() for _ in range(count)]
    filename = "cookies.txt"

    with open(filename, "w") as f:
        f.write("\n".join(cookies))

    with open(filename, "rb") as f:
        await context.bot.send_document(chat_id, f, filename=filename, caption=f"✅ {count} кук сгенерированы")

    os.remove(filename)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
