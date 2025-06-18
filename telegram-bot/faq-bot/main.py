import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes


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
    keyboard = [
        [InlineKeyboardButton(title, callback_data=title)]
        for title in faq_data.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Silakan pilih kategori FAQ:", reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data in faq_data:
        sub_questions = faq_data[data]
        keyboard = [
            [InlineKeyboardButton(sub_q, callback_data=f"{data}|{sub_q}")]
            for sub_q in sub_questions.keys()
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"📂 {data}:\nPilih pertanyaan:", reply_markup=reply_markup)
    elif "|" in data:
        category, question = data.split("|")
        answer = faq_data[category][question]
        await query.edit_message_text(f"❓ {question}\n\n💬 {answer}")


def main():
    app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
