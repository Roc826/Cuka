from nonebot import on_command, CommandSession
from .freegame import get_free_game
@on_command('freegame', aliases=('免费游戏', 'steam游戏', '游戏日报'))
async def freegame(session: CommandSession):
    freegame_report = await get_free_game()
    await session.send(freegame_report)
