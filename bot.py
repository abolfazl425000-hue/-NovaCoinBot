import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes


TOKEN = os.getenv("BOT_TOKEN")

WEB_APP_URL = "https://abolfazl425000-hue.github.io/-NovaCoinBot/"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """🪙 به NovaCoin خوش آمدید!

👆 با هر ضربه روی سکه، 1 Nova دریافت کنید.

⚡ انرژی خود را مدیریت کنید.
🎁 مأموریت‌ها و پاداش‌های روزانه در راه هستند.
👥 دوستانتان را دعوت کنید و پاداش بیشتری بگیرید.
🏆 برای رسیدن به رتبه‌های بالاتر تلاش کنید.

🚀 همین حالا وارد Nova شوید و استخراج را شروع کنید!"""

    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Play Nova",
                web_app={"url": WEB_APP_URL}
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )


def main():

    if not TOKEN:
        raise RuntimeError("BOT_TOKEN تنظیم نشده است")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    print("NovaCoinBot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
