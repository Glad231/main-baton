import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.INFO)

TOKEN = "8784344056:AAGDeL1uFYl6ozfb9kke5blB7y9Tsb28pVo"
ADMIN_ID = 1076952379
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")

def save_user(user):
    user_id = user.id
    username = user.username if user.username else "no_username"
    try:
        with open("users.txt", "r") as f:
            users = f.read().splitlines()
    except:
        users = []
    user_line = f"{user_id}|{username}"
    if not any(user_line == u for u in users):
        with open("users.txt", "a") as f:
            f.write(user_line + "
")

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
    user = update.effective_user
    user_id = user.id
    save_user(user)
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
        await update.message.reply_text("Бот с видео, проэкт начинающего програмиста с Сиряков ;) 🎬")
    
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
        text_users = "
".join(users)
        await update.message.reply_text(f"📋 Список:
{text_users}")
    elif text == "📢 Рассылка" and user_id == ADMIN_ID:
        context.user_data["broadcast"] = True
        await update.message.reply_text("✍️ Напиши сообщение для рассылки:")
    elif context.user_data.get("broadcast") and user_id == ADMIN_ID:
        users = get_users()
        success = 0
        for user in users:
            try:
                u_id = int(user.split("|")[0])
                await context.bot.send_message(chat_id=u_id, text=text)
                success += 1
            except:
                pass
        context.user_data["broadcast"] = False
        await update.message.reply_text(f"✅ Отправлено: {success}")
    elif text == "🔙 Назад":
        await update.message.reply_text(
            "Главное меню 👇",
            reply_markup=get_main_keyboard(user_id)
        )
    else:
        await update.message.reply_text("Выбери кнопку 👇")

ptb_app = ApplicationBuilder().token(TOKEN).updater(None).build()
ptb_app.add_handler(CommandHandler("start", start))
ptb_app.add_handler(MessageHandler(filters.TEXT, handle_buttons))

@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_url = f"{RENDER_URL}/webhook"
    logging.info(f"Регистрация вебхука в Telegram: {webhook_url}")
    await ptb_app.bot.set_webhook(url=webhook_url)
    async with ptb_app:
        await ptb_app.initialize()
        await ptb_app.start()
        yield
        await ptb_app.stop()
        await ptb_app.shutdown()

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def process_update(request: Request):
    req_data = await request.json()
    update = Update.de_json(req_data, ptb_app.bot)
    await ptb_app.process_update(update)
    return Response(status_code=200)

@app.get("/")
async def health_check():
    return {"status": "working"}
