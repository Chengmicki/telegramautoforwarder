
# Telegram Message Forwarder Bot

This is a dual Telegram bot built using **Telethon** (userbot) and **python-telegram-bot** (Bot API) to automatically **forward messages from specified source channels to a destination channel**.

---

## ✨ Features

- 📨 Forwards messages from specific source channels to a destination channel.
- ✅ Skips duplicate messages.
- ⏳ Forwards new messages automatically as they arrive.
- 🔄 Robust: Reconnects and retries on network failure.
- 🔧 Easy to configure source and destination IDs.

---

## 🛠️ Requirements

- Python 3.8+
- Telegram API credentials (API ID & API Hash)
- Telegram Bot Token

---

## 📦 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Chengmicki/telegramautoforwarder.git
cd telegram-forwarder
2. Create a Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # or `venv\Scripts\activate` on Windows
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Configuration
Update the following values directly in main.py:

python
Copy
Edit
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

SOURCE_CHANNELS = [-1001234567890, -1009876543210]  # Add as many as you want
DESTINATION_CHANNEL = -1001122334455
Replace the API_ID, API_HASH, and BOT_TOKEN with your own values.
Use full chat_id (not usernames) for channels, including the -100 prefix.