"""Start other modules automatically"""

from loguru import logger

import modules.helpers.errorhandle as eh
import modules.helpers.config as cn

import modules.message as message
import modules.profile as profile
import modules.online as online
import modules.story as story
import modules.photo as photo

logger = logger.opt(colors=True)


async def start_static_trackers(client) -> None:
    logger.trace("Starting static info trackers, timings=<y>{}</>...",
                 "[deprecated]")

    for user_info in cn.get(["targets", "users"]):
        await eh.log(client.loop.create_task(profile.main(client, user_info)))
        await eh.log(client.loop.create_task(story.main(client, user_info)))
        await eh.log(client.loop.create_task(photo.main(client, user_info)))
        await eh.log(client.loop.create_task(online.main(client, user_info)))

async def start_message_handlers(client, event) -> None:
    logger.trace("Starting message handlers...")
    await eh.log(message.main(client, event))
