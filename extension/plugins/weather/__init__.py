from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from .data_source import get_weather_of_city, is_json
from jieba import posseg
import json

@on_command('weather', aliases=('天气', '天气预报', '查天气'))
async def weather(session: CommandSession):
    city = session.get('city', prompt='你想查询哪个城市的天气呢？')
    date = session.get('date')
    weather_report = await get_weather_of_city(city,date)
    await session.send(weather_report)


@weather.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    searchInfo={'city': None,
               'date': 0}

    if session.is_first_run:
        if stripped_arg:
            if is_json(stripped_arg):
                searchInfo = json.loads(stripped_arg)
                session.state['city'] = searchInfo['city']
                session.state['date'] = searchInfo['date']
            else:
                session.state['city'] = stripped_arg
                session.state['city'] = 0
        return
    else:
        searchInfo['city'] = stripped_arg

    if not searchInfo['city']:
        session.pause('要查询的城市名称不能为空呢，请重新输入')
    session.state[session.current_key] = searchInfo

@on_natural_language(keywords={'天气','weather'},only_to_me=False)
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg = session.msg_text.strip()
    # 对消息进行分词和词性标注
    words = posseg.lcut(stripped_msg)
    dates = {'今天': 0,
             '明天': 1,
             '后天': 2
             }
    searchInfo={'city': None,
                'date': None}
    # 遍历 posseg.lcut 返回的列表
    for word in words:
        # 每个元素是一个 pair 对象，包含 word 和 flag 两个属性，分别表示词和词性
        if word.flag == 'ns' and searchInfo['city'] is None:
            # ns 词性表示地名
            searchInfo['city'] = word.word
        if word.flag == 't' and searchInfo['date'] is None:
            if word.word in dates:

                searchInfo['date'] = dates[word.word]
        if (not searchInfo['city'] is None) and ( not searchInfo['date'] is None):
            break
    if searchInfo['date'] is None:
        searchInfo['date'] =0

    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(80.0, 'weather', current_arg=json.dumps(searchInfo) or '')