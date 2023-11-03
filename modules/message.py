"""Save info about message into output"""

import time

from loguru import logger

import modules.helpers.output as ot

logger = logger.opt(colors=True)


async def main(client, data, event):
    """Save info about message into output"""
    logger.debug("Saving info about message, event=<w>{}</>",
                 event)
    m = event.message
    s = event.sender

    headers = {"time": "int", "msg_id": "int", "sender_id": "int",
               "message": "str", "media_path": "int", "is_out": "bool",
               "mentioned": "bool", "silent": "bool",
               "from_scheduled": "bool", "via_bot_id": "int",
               "forwards": "int", "grouped_id": "int",
               "fwd_from_id": "int", "reply_to_msg_id": "int"}

    m_time = int(time.time())
    sender_id = s.id

    if m.fwd_from:
        logger.trace("Message <y>{}</> is forwarded", m.id)
        fwd_from_id = m.fwd_from.from_id.id
    else:
        logger.trace("Message <y>{}</> isn't forwarded", m.id)
        fwd_from_id = None

    if m.reply_to:
        logger.trace("Message <y>{}</> contains a reply", m.id)
        reply_to_msg_id = m.reply_to.reply_to_msg_id
    else:
        logger.trace("Message <y>{}</> doesn't contain a reply", m.id)
        reply_to_msg_id = None

    if m.media:
        logger.trace("Message <y>{}</> contains a media", m.id)
        media = await client.download_media(m, "output/media/")
    else:
        logger.trace("Message <y>{}</> doesn't contain a media", m.id)
        media = None


    results = [m_time, m.id, sender_id, m.message, media, m.out,
               m.mentioned, m.silent, m.from_scheduled, m.via_bot_id,
               m.forwards, m.grouped_id, fwd_from_id, reply_to_msg_id]
    logger.trace("Got results=<w>{}</>", results)

    await ot.save_record("message", data["output"], headers, results)
