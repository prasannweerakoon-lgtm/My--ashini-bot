from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8991170293:AAG5vKqliqui-kdE3P6ERhchv-dNrNtr4Sc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Group Management Bot is active.")

async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message and message.text:
        text = message.text.lower()
        if "http://" in text or "https://" in text or "t.me/" in text or "www." in text:
            try:
                await message.delete()
                await context.bot.send_message(
                    chat_id=message.chat_id,
                    text=f"Warning! @{message.from_user.username} Links are not allowed in this group!"
                )
            except Exception as e:
                print(f"Error: {e}")

async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.reply_to_message:
        user_to_kick = message.reply_to_message.from_user.id
        try:
            await context.bot.ban_chat_member(chat_id=message.chat_id, user_id=user_to_kick)
            await context.bot.unban_chat_member(chat_id=message.chat_id, user_id=user_to_kick)
            await message.reply_text("User has been kicked from the group.")
        except Exception as e:
            await message.reply_text("Failed to kick user. Make sure I am an Admin!")
    else:
        await message.reply_text("Reply to a user's message with /kick to remove them.")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("kick", kick_user))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), delete_links))

print("Bot is running with Group Admin features...")
app.run_polling()
