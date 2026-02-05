from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from utils import save_chat, remove_chat, get_saved_chats
import asyncio

class Bot:
    def __init__(self, secret):
        self.secret = secret
        self.chats = set()
        self.app = None
        self.loop = None

    async def post_init(self, app: Application):
        """Callback to capture the running event loop."""
        self.loop = asyncio.get_running_loop()

    async def broadcast_msg(self, msg):
        for chat in list(self.chats):
            try:
                await self.app.bot.send_message(chat, msg)
            except Exception as e:
                print(f"Failed to send to {chat}: {e}")

    def broadcast_msg_sync(self, msg):
        """Thread-safe method to call broadcast_msg from another thread."""
        if self.loop:
            asyncio.run_coroutine_threadsafe(self.broadcast_msg(msg), self.loop)

    def load_chats(self):
        for chat in get_saved_chats():
            self.chats.add(chat)

    async def subscribe(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.message.chat_id
        if not chat_id in self.chats:
            self.chats.add(chat_id)
            save_chat(chat_id)
        await update.message.reply_text('You have subscribed succesfully!')

    async def unsubscribe(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.message.chat_id
        if chat_id in self.chats:
            self.chats.remove(chat_id)
            remove_chat(chat_id)
            await update.message.reply_text('You have unsubscribed succesfully!')

    def start_bot(self):
        self.app = Application.builder().token(self.secret).post_init(self.post_init).build()
        self.load_chats()
        
        self.app.add_handler(CommandHandler(['start', 'subscribe'], self.subscribe))
        self.app.add_handler(CommandHandler(['stop', 'unsubscribe'], self.unsubscribe))
        
        print("Bot is running!")
        self.app.run_polling()
        self.loop = asyncio.get_event_loop()