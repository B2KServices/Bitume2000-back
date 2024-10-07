import threading
import asyncio
from setup import create_app, bot

app = create_app()

def run_app():
    app.run(host='0.0.0.0', port=5001, debug=False)

async def run_bot():
    await bot.start()

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_app)

    flask_thread.run()

    asyncio.run(run_bot())

    flask_thread.join()
