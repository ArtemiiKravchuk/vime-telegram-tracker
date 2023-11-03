"""Track Telegram stats for a particular user/group/channel"""

import sys
import json
import time
import signal
import asyncio
import logging

from loguru import logger

from telethon import TelegramClient, events

import modules.start as st

logger.debug("Retrieving info from config.json")
with open("config.json", "r", encoding="UTF-8") as file:
    data = json.load(file)

logger.info("Configuring logging and loguru")
logging.basicConfig(filename='logs/telethon.log', encoding='utf-8',
                    level=logging.DEBUG)

logger.remove()
logger.add("logs/journal.log", level="TRACE", rotation="50 MB",
           format=data["advanced"]["loguru_format"], enqueue=True)
logger.add(sys.stderr, format=data["advanced"]["loguru_format"],
           level="TRACE", enqueue=True)
logger = logger.opt(colors=True)


def signal_handler(sig, frame):
    logger.error("Got SIGINT, frame=<w>{}</>", frame)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


async def static_info_tracker(timings: str):
    """Start a loop for keeping track of static data (profile pics,
    bio, etc)"""
    logger.info("Starting static info tracking")
    loop_counter = 0
    while True:
        if loop_counter == 0:
            logger.trace("First time using static info tracker, sleep 2 s")
            await asyncio.sleep(2)

        logger.debug("For static info tracker, loop_counter=<y>{}</>",
                     loop_counter)
        await st.start_static_trackers(client, data, timings)
        loop_counter += 1

        sleep_time = data["static_info_tracking_timings"][f"{timings}_s"]
        logger.trace("Sleeping <y>{}</> sec...", sleep_time)
        await asyncio.sleep(sleep_time)


async def new_message_handler(event):
    """Handle new incoming message"""
    sender = event.sender
    logger.opt(ansi=True).debug(
        f"Handling incoming message from <w>{sender}</>")
    await st.start_message_handlers(client, data, event)


def main() -> None:
    """Connect to a session and run the script"""
    global client
    logger.info("Running the script by calling main()")

    logger.debug("Retrieving info of TG_CORE from config.json")
    api_id = data["telegram"]["api_id"]
    api_hash = data["telegram"]["api_hash"]

    logger.info("Connecting to client...")
    client = TelegramClient('sessions/client', api_id, api_hash,
                            flood_sleep_threshold=3600)

    logger.debug("Defining correct event handlers")
    client.add_event_handler(new_message_handler, events.NewMessage)
    client.loop.create_task(static_info_tracker("standart"))
    client.loop.create_task(static_info_tracker("frequent"))

    logger.info(
        "Starting the client, running until disconnected...")
    client.start()
    client.run_until_disconnected()


if __name__ == "__main__":
    logger.info('__name__ = "__main__", starting the script')
    main()
