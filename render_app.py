import os
import threading
from flask import Flask
from bot import start   # <-- correct function

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive 🚀"


def run_bot():
    start()   # <-- correct call


threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
