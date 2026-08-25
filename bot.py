import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from supabase import create_client, Client


TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

WEB_APP_URL = "https://abolfazl425000-hue.github.io/-NovaCoinBot/"


if not TOKEN:
    raise RuntimeError("BOT_TOKEN تنظیم نشده است")

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL تنظیم نشده است")

if not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_KEY تنظیم نشده است")


supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    if not user:
        return

    telegram_id = user.id
    username = user.username
    first_name = user.first_name or "کاربر Nova"

    try:

        result = (
            supabase
            .table("users")
            .select("telegram_id,balance,energy")
            .eq("telegram_id", telegram_id)
            .execute()
        )

        if not result.data:

            supabase.table("users").insert({
                "telegram_id": telegram_id,
                "username": username,
                "first_name": first_name,
                "balance": 0,
                "energy": 1000,
                "max_energy": 1000
            }).execute()

        else:

            supabase.table("users").update({
                "username": username,
                "first_name": first_name
            }).eq(
                "telegram_id",
                telegram_id
            ).execute()

    except Exception as error:

        print("Supabase error:", error)

    text = f"""🪙 به NovaCoin خوش آمدید!

سلام {first_name} 👋

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
                web_app={
                    "url": WEB_APP_URL
                }
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(
        keyboard
    )

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )


def main():

    app = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    print(
        "NovaCoinBot is running..."
    )

    app.run_polling()


if __name__ == "__main__":
    main()
