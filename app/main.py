import asyncio
from concurrent.futures import ThreadPoolExecutor

from setup import bot, create_app

app = create_app()


def run_app():
    app.run(host='0.0.0.0', port=5001, debug=False)


async def run_bot():
    await bot.run()


def main():
    executor = ThreadPoolExecutor(max_workers=2)

    flask_future = executor.submit(run_app)
    bot_future = executor.submit(asyncio.run, bot.run())

    flask_future.result()
    bot_future.result()


if __name__ == '__main__':
    main()
