from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = "8784344056:AAGDeL1uFYl6ozfb9kke5blB7y9Tsb28pVo"
ADMIN_ID = 1076952379

def save_user(user_id):
    try:
        with open("users.txt", "r") as f:
            users = f.read().splitlines()
    except:
        users = []

    if str(user_id) not in users:
        with open("users.txt", "a") as f:
            f.write(str(user_id) + "\n")

def get_users():
    try:
        with open("users.txt", "r") as f:
            return f.read().splitlines()
    except:
        return []


def get_main_keyboard(user_id):
    keyboard = [
        ["🎬 Видео 1", "📷 Фото 1"],
        ["🎬 Видео 2", "📷 Фото 2"],
        ["🎬 Видео 3"],
        ["ℹ️ О боте"]
    ]

    if user_id == ADMIN_ID:
        keyboard.append(["⚙️ Админ панель"])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_admin_keyboard():
    keyboard = [
        ["📊 Статистика", "📋 Пользователи"],
        ["📢 Рассылка"],
        ["🔙 Назад"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)

    await update.message.reply_text(
        "Привет, выбери 👇",
        reply_markup=get_main_keyboard(user_id)
    )

async def send_video(update, context, filename):
    await context.bot.send_video(
        chat_id=update.effective_chat.id,
        video=open(filename, "rb")
    )

async def send_photo(update, context, filename):
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(filename, "rb")
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "🎬 Видео 1":
        await send_video(update, context, "video1.mp4")

    elif text == "🎬 Видео 2":
        await send_video(update, context, "video2.mp4")

    elif text == "🎬 Видео 3":
        await send_video(update, context, "video3.mp4")

    elif text == "📷 Фото 1":
        await send_photo(update, context, "photo1.jpg")

    elif text == "📷 Фото 2":
        await send_photo(update, context, "photo2.jpg")

    elif text == "ℹ️ О боте":
        await update.message.reply_text("Бот с видео 🎬")

 
    elif text == "⚙️ Админ панель" and user_id == ADMIN_ID:
        await update.message.reply_text(
            "👑 Админ панель",
            reply_markup=get_admin_keyboard()
        )

    elif text == "📊 Статистика" and user_id == ADMIN_ID:
        users = get_users()
        await update.message.reply_text(f"👥 Пользователей: {len(users)}")

    elif text == "📋 Пользователи" and user_id == ADMIN_ID:
        users = get_users()
        text_users = "\n".join(users)
        await update.message.reply_text(f"📋 Список:\n{text_users}")

    elif text == "📢 Рассылка" and user_id == ADMIN_ID:
        context.user_data["broadcast"] = True
        await update.message.reply_text("✍️ Напиши сообщение для рассылки:")

    elif context.user_data.get("broadcast") and user_id == ADMIN_ID:
        users = get_users()
        for user in users:
            try:
                await context.bot.send_message(chat_id=user, text=text)
            except:
                pass

        context.user_data["broadcast"] = False
        await update.message.reply_text("✅ Рассылка отправлена")

    elif text == "🔙 Назад":
        await update.message.reply_text(
            "Главное меню 👇",
            reply_markup=get_main_keyboard(user_id)
        )

    else:
        await update.message.reply_text("Выбери кнопку 👇")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_buttons))

app.run_polling()
