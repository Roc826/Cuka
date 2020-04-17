from nonebot import on_command, CommandSession
from .shangxueba import get_answer_report
@on_command('s', aliases=('上学吧', 'sxb'))
async def get_answer(session: CommandSession):
    question_id = session.get('question_id', prompt='你想查询的问题编号')
    answer = await get_answer_report(question_id)
    await session.send(answer)

