from .main import main, listen_to_redis

import asyncio
import logging
from threading import Thread, Event

stop_event = Event()

def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    listen_thread = Thread(target=listen_to_redis, args=(stop_event,))
    listen_thread.daemon = True
    listen_thread.start()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        stop_event.set()
        listen_thread.join()

if __name__ == "__main__":
    start()