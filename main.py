import os
import re
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# Load environment variables
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize Telethon client
userbot = TelegramClient("user_session", API_ID, API_HASH)

# Store user configurations
user_configs = {}

# --- Telegram Bot Logic ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to AutoForwarderBot!\n\n"
        "✅ Step 1: Please *forward a message* from your **source channel** "
        "(or send its @username or channel ID)."
    )
    user_configs[update.message.from_user.id] = {"step": 1}

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text
    config = user_configs.get(user_id, {})

    if config.get("step") == 1:
        # Extract source channel
        if update.message.forward_from_chat:
            source = update.message.forward_from_chat.id
        else:
            source = text.strip()
        config["source"] = source
        config["step"] = 2
        await update.message.reply_text(
            "✅ Got it!\n\nStep 2: Now *forward a message* from your **destination channel** "
            "(or send its @username or ID)."
        )

    elif config.get("step") == 2:
        if update.message.forward_from_chat:
            dest = update.message.forward_from_chat.id
        else:
            dest = text.strip()
        config["destination"] = dest
        config["step"] = 3
        await update.message.reply_text(
            "✅ Done!\n\n🔁 I will now forward messages every 5 minutes.\n\n"
            "✏️ If you'd like to replace any @username in messages, send the preferred username now (e.g. `@yourname`)."
        )

    elif config.get("step") == 3:
        if text.startswith("@"):
            config["replace_username"] = text.strip()
            await update.message.reply_text(
                f"🔄 Any @usernames in posts will now be changed to: `{text.strip()}`"
            )
        else:
            await update.message.reply_text("❗ Please send a valid username (must start with @).")

    user_configs[user_id] = config

# --- Telethon Forwarding Task (Runs Every 5 Minutes) ---
async def forward_loop():
    last_message_id = {}

    while True:
        for user_id, config in user_configs.items():
            try:
                source = config["source"]
                dest = config["destination"]
                replace_with = config.get("replace_username", None)

                # Get last 1 message
                messages = await userbot.get_messages(source, limit=1)
                if not messages:
                    continue

                msg = messages[0]
                if last_message_id.get(user_id) == msg.id:
                    continue  # skip if already forwarded

                # Replace @usernames if configured
                text = msg.message or ""
                if replace_with:
                    text = re.sub(r"@[\w\d_]+", replace_with, text)

                # Send to destination
                await userbot.send_message(dest, text, file=msg.media if msg.media else None)
                last_message_id[user_id] = msg.id
                print(f"✅ Forwarded message for user {user_id}")
            except Exception as e:
                print(f"❌ Error forwarding for user {user_id}: {e}")
        await asyncio.sleep(300)  # Wait 5 minutes

# --- Main Runner ---
async def main():
    await userbot.start()
    print("✅ Telethon userbot connected.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    print("🤖 Telegram bot is running...")

    await asyncio.gather(
        userbot.loop.create_task(forward_loop()),
        app.run_polling()
    )

# Windows-safe launcher
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
