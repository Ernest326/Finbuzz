from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler
import asyncio

class Bot:
    def __init__(self, secret):
        self.secret = secret
        self.chats = set()
        self.app = None

    async def broadcast_msg(self, msg):
        for chat in self.app.bot.get_chats():
            try:
                await self.app.bot.send_message(chat, msg)
            except e:
                print(f"Failed to send {chat}: {e}")

    def broadcast_msg_sync(self, msg):
        if self.app and self.app.loop:
            asyncio.run_coroutine_threadsafe(self.broadcast_msg(msg), self.app, self.app.loop)

    async def unsubscribe(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.message.chat_id
        self.chats.remove(chat_id)
        await update.message.reply_text('You have unsubscribed succesfully!')

    async def subscribe(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.message.chat_id
        self.chats.add(chat_id)
        await update.message.reply_text('You have subscribed succesfully!')


    def start_bot(self):
        app = Application.builder().token(self.secret).build()
        self.app = app
        self.bot = app.bot

        app.add_handler(CommandHandler(['start', 'subscribe'], self.subscribe))
        app.add_handler(CommandHandler(['stop', 'unsubscribe'], self.unsubscribe))
        print("Bot is running!")
        self.app.run_polling()