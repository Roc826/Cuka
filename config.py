from nonebot.default_config import *
import re

API_ROOT = 'http://127.0.0.1:5700'
HOST = '0.0.0.0'
PORT = 8785
DEBUG = True
SUPERUSERS = {455050572}
NICKNAME = ['龙王']
COMMAND_START = {'','/', '!',re.compile(r'[/!]+')}
COMMAND_SEP = {'.'}
SESSION_EXPIRE_TIMEOUT = timedelta(minutes=2)
SESSION_RUN_TIMEOUT = timedelta(seconds=10)
SESSION_RUNNING_EXPRESSION = '我回复不过来了啦'
SHORT_MESSAGE_MAX_LENGTH = 100
DEFAULT_VALIDATION_FAILURE_EXPRESSION = '你发送的内容格式不太对呢，请检查一下再发送哦～'
TOO_MANY_VALIDATION_FAILURES_EXPRESSION = (
    '你输错太多次啦，需要的时候再叫我吧',
    '你输错太多次了，建议先看看使用帮助哦～',
)
SESSION_CANCEL_EXPRESSION = (
    '好的',
    '好的吧',
    '好吧，那奶茶就不打扰啦',
    '那奶茶先不打扰小主人啦',
)
