from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import os
import asyncio
from dotenv import load_dotenv
from methods import To_Do_List 
from db import db

application = None

def main():
    global application, loop
    try:
        load_dotenv()
        BOT_TOKEN = os.getenv("BOT_TOKEN")
        
        # 1. Initialize database setup
        asyncio.run(db.init_db())
        
        # 2. Build the application and store it globally
        application = Application.builder().token(BOT_TOKEN).build()
        
        # 3. Register command handlers (Your existing handlers)
        application.add_handler(CommandHandler("start", To_Do_List.start))
        application.add_handler(CommandHandler("add", To_Do_List.add))
        application.add_handler(CommandHandler("help", To_Do_List.help))
        application.add_handler(CommandHandler("list", To_Do_List.list))
        application.add_handler(CommandHandler("done", To_Do_List.done))
        application.add_handler(CommandHandler("clear", To_Do_List.clear))
        application.add_handler(CallbackQueryHandler(To_Do_List.clear_callback, pattern="clear_"))
        application.add_handler(CallbackQueryHandler(To_Do_List.done_callback, pattern="^done:"))
        application.run_polling()
        
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # No Windows-specific policy needed here.
    main()