from telegram import InlineQueryResultArticle, InputTextMessageContent, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, InlineQueryHandler, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN, API_BASE_URL
from services.api_client import get_data

TOKEN = TELEGRAM_TOKEN
url = API_BASE_URL
# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Inline rejimda ishlating: @it_park_2_bot kalit_so'z.")

# Inline query funksiyasi
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query

    if not query or len(query) < 2:
        return   
    query = url + "v1/jobs/?search=" + query
    print(query)
    results = get_data(query=query)
    responses = []
    if results['count'] == 0:
        responses.append(
            InlineQueryResultArticle(
                id="1",
                title="Natija topilmadi",
                input_message_content=InputTextMessageContent("Kechirasiz, bu so'z bo'yicha natija topilmadi.")
            )
        )
        await update.inline_query.answer(responses, cache_time=1)
        return
    jobs = results['results']
    for job in jobs:
        responses.append(
            InlineQueryResultArticle(
            id=job['id'],
            title=job['name'],
            thumbnail_url=job['company_image'],
            description=f"{job['company_sity']} - {job['company_salary']}",
            input_message_content=InputTextMessageContent(f"{job['company_salary']}\n<b>{job['company_sity']}</b>"+f"\n{job['link']}",parse_mode='HTML'),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Saytga kirish", url=job['link'])]
                ]
             )
        ),
        
        )

    await update.inline_query.answer(responses, cache_time=1)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(InlineQueryHandler(inline_query))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
