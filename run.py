import asyncio
import schedule
import time

from sweter.searchers import run_searcher


def task():
    try:
        asyncio.run(run_searcher())
    except Exception as e:
        print("Error on task" + e)


schedule.every(10).minutes.do(task)


def start():
    while True:
        schedule.run_pending()

        time.sleep(5)


if __name__ == "__main__":
    start()
