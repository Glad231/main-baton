
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = "8784344056:AAGDeL1uFYl6ozfb9kke5blB7y9Tsb28pVo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🎬 Видео 1", "📷 Фото 1" ],
        ["🎬 Видео 2", "📷 Фото 2" ],
        ["🎬 Видео 3"],
        ["ℹ️ О боте"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Привет, выбери видео 👇",
        reply_markup=reply_markup
    )

async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE, filename):
    await context.bot.send_video(
        chat_id=update.effective_chat.id,
        video=open(filename, "rb")
    )

async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE, filename):
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(filename, "rb")
    )
    
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

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
        await update.message.reply_text("Бот с видео, начало проэкта молодого програмиста 😊 🎬")

    else:
        await update.message.reply_text("Выбери кнопку 👇")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_buttons))

app.run_polling()
