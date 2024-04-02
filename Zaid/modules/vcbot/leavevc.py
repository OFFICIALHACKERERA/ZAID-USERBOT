from asyncio.queues import QueueEmpty
from pyrogram import filters
from pytgcalls.exceptions import GroupCallNotFound

from ... import *
from ...modules.mongo.streams import *
from ...modules.utilities import queues


@app.on_message(cdx(["lve", "leave", "leavevc"]) & ~filters.private)
@sudo_users_only
async def leave_vc(client, message):
    chat_id = message.chat.id
    try:
        a = await call.get_call(chat_id)
        if (a.status == "not_playing"
            or a.status == "playing"
            or a.status == "paused"
        ):  
            try:
                queues.clear(chat_id)
            except QueueEmpty:
                pass
            await call.leave_group_call(chat_id)
            await eor(message, "**Left VC!**")
    except GroupCallNotFound:
        await eor(message, "**I am Not in VC!**")
    except Exception as e:
        print(f"Error: {e}")
      
