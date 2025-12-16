from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List
from db import db

class To_Do_List:
    async def start(update, context):
        welcome_text = (
            "👋 *Hello! Welcome to your To-Do List Bot!*\n\n"
            "I can help you manage your tasks easily. Here's what you can do:\n"
            " Add tasks using /add\n"
            " View tasks using /list\n"
            " Mark tasks as done using /done\n"
            " Clear all tasks using /clear\n\n"
            "Type /help anytime to see all commands.\n"
            "PS: More commands coming soon..."
        )

        await update.message.reply_text(welcome_text, parse_mode="Markdown")

    async def help(updates, context):
        help_text = (
            "📌 *To-Do List Bot Commands*\n\n"
            "➕ /add <task>\n"
            "Add a new task to your list\n\n"
            "📋 /list\n"
            "View all pending tasks\n\n"
            "✅ /done\n"
            "Mark a task as completed\n\n"
            "🗑️ /clear\n"
            "Clear all your tasks\n\n"
            "ℹ️ /help\n"
            "Show this help message"
        )

        await updates.message.reply_text(help_text, parse_mode="Markdown")

    async def add(updates,context):
        if not context.args:
            await updates.message.reply_text("Please provide a task to add!")
            return
        
        user_id = updates.message.from_user.id
        task = " ".join(context.args)
        task_id = await db.add_task(user_id,task)
        await updates.message.reply_text(f"Task added succesfully! The task id is {task_id}")
        return

    async def list(updates, context):

        user_id = updates.message.from_user.id

        message = await db.list_task(user_id)
        
        await updates.message.reply_text(message, parse_mode = "Markdown")

    async def done(updates,context):
        user_id = updates.message.from_user.id
        tasks : List = await db.get_uncompleted_tasks(user_id)
        if not tasks:
            await updates.message.reply_text(f"There are no pending tasks 🎉")
            return
        keyboard = []

        for task_id, task_text in tasks:
            text = task_text[:40] + "..." if len(task_text) > 40 else task_text
            keyboard.append([
                InlineKeyboardButton(
                    text=text,
                    callback_data=f"done:{task_id}"
                )
            ])
        
        await updates.message.reply_text(
        "Select a task to mark as completed:",
        reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    async def done_callback(updates, context):
        query = updates.callback_query
        await query.answer()

        user_id = query.from_user.id
        data = query.data 

        # Safety check
        if not data.startswith("done:"):
            return

        try:
            task_id = int(data.split(":")[1])
        except (IndexError, ValueError):
            await query.edit_message_text("❌ Invalid task selection.")
            return
        
        success = await db.mark_task_completed(user_id, task_id)

        if success:
            await query.edit_message_text("✅ Task marked as completed!\nUse /done again to mark more.")
        else:
            await query.edit_message_text(
                "⚠️ This task was not found, already completed, or does not belong to you."
            )
        return 


    async def clear(updates,context):
        keyboard = [
            [
                InlineKeyboardButton("yes",callback_data="clear_yes"),
                InlineKeyboardButton("no",callback_data="clear_no"),
            ]
        ]
        await updates.message.reply_text(
        "Are you sure you want to clear all tasks?",
        reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return 
    
    async def clear_callback(updates, context):
        query = updates.callback_query
        await query.answer()

        user_id = query.from_user.id
        data = query.data

        if data == "clear_yes":
            deleted_count = await db.clear_tasks(user_id)

            if deleted_count == 0:
                await query.edit_message_text("Your task list is already empty 🎉")
            else:
                await query.edit_message_text(
                    f"🗑️ Cleared {deleted_count} task(s) successfully!"
                )

        else:
            await query.edit_message_text("❎ Clear operation cancelled.")


    