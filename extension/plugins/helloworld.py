from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.typing import *
import nonebot
from config import *

bot = nonebot.get_bot()
@on_command('test',only_to_me=False)
async def test(session: CommandSession):
        await session.send("nonebot test success")
#@bot.on_message('group')
#async def handle_group_message(ctx: Context_T):
#    await bot.send_group_msg(group_id=groupinfo['groupId'], message=ctx['raw_message'])
