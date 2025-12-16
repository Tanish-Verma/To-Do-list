from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import os
from dotenv import load_dotenv
from methods import To_Do_List
from db import db
import asyncio

def main():
    load_dotenv()

    BOT_TOKEN = os.environ["BOT_TOKEN"]
    WEBHOOK_URL = os.environ["WEBHOOK_URL"]
    PORT = int(os.environ.get("PORT", 8000))

    asyncio.run(db.init_db())

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", To_Do_List.start))
    application.add_handler(CommandHandler("add", To_Do_List.add))
    application.add_handler(CommandHandler("help", To_Do_List.help))
    application.add_handler(CommandHandler("list", To_Do_List.list))
    application.add_handler(CommandHandler("done", To_Do_List.done))
    application.add_handler(CommandHandler("clear", To_Do_List.clear))
    application.add_handler(CallbackQueryHandler(To_Do_List.clear_callback, pattern="^clear_"))
    application.add_handler(CallbackQueryHandler(To_Do_List.done_callback, pattern="^done:"))

    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
    )

if __name__ == "__main__":
    main()
