import os
import threading
from flask import Flask
from bot import main as start_bot

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive 🚀"


def run_bot():
    start_bot()


# start telegram bot in background thread
threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
