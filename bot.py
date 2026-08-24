import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]


def menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⛏ Mine NVA", callback_data="mine"),
            InlineKeyboardButton("👤 Profile", callback_data="profile")
        ],
        [
            InlineKeyboardButton("🎁 Daily", callback_data="daily"),
            InlineKeyboardButton("👥 Referral", callback_data="referral")
        ],
        [
            InlineKeyboardButton("🏆 Ranking", callback_data="ranking")
        ]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Welcome to Nova!\n\n"
        "🪙 Token: NVA\n\n"
        "Choose an option:",
        reply_markup=menu()
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "mine":
        await query.message.reply_text(
            "⛏ Mining successful!\n\n"
            "+10 NVA"
        )

    elif query.data == "profile":
        await query.message.reply_text(
            f"👤 Profile\n\n"
            f"User ID: {query.from_user.id}"
        )

    elif query.data == "daily":
        await query.message.reply_text(
            "🎁 Daily reward!\n\n"
            "+50 NVA"
        )

    elif query.data == "referral":
        bot = await context.bot.get_me()
        link = f"https://t.me/{bot.username}?start={query.from_user.id}"

        await query.message.reply_text(
            "👥 Your referral link:\n\n"
            f"{link}"
        )

    elif query.data == "ranking":
        await query.message.reply_text(
            "🏆 Nova Ranking\n\n"
            "1. Coming soon..."
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("NovaCoinBot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
