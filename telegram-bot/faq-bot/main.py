import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes


BOT_TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

faq_data = {
    "Layanan Kami": {
        "Apa saja layanan yang ditawarkan?": "Kami menawarkan layanan A, B, dan C.",
        "Bagaimana cara mendaftar?": "Anda bisa mendaftar melalui website kami di halaman 'Daftar'."
    },
    "Pembayaran": {
        "Metode pembayaran yang didukung?": "Kami mendukung transfer bank, e-wallet, dan kartu kredit.",
        "Apakah bisa cicilan?": "Saat ini belum tersedia sistem cicilan."
    },
    "Kontak": {
        "Bagaimana cara menghubungi kami?": "Anda bisa hubungi kami via email: support@example.com."
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"User {user.id} ({user.first_name}) started the bot.")
    keyboard = [
        [InlineKeyboardButton(title, callback_data=title)]
        for title in faq_data.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Silakan pilih kategori FAQ:", reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    data = query.data
    logger.info(f"User {user.id} ({user.first_name}) clicked: {data}")

    if data in faq_data:
        sub_q = faq_data[data]
        keyboard = [
            [InlineKeyboardButton(q, callback_data=f"{data}|{q}")]
            for q in sub_q
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"📂 {data}:\nPilih pertanyaan:", reply_markup=reply_markup)
    elif "|" in data:
        cat, q = data.split("|")
        answer = faq_data[cat][q]
        await query.edit_message_text(f"❓ {q}\n\n💬 {answer}")
        logger.info(f"Answered: {q} -> {answer}")

def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN is not set!")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    logger.info("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
