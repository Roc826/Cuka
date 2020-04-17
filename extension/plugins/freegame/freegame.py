from selenium import webdriver
from selenium.webdriver.firefox.options import Options as firfoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from datetime import datetime,timezone,timedelta
from dateutil.parser import parse

def get_html():
    url="https://steamdb.info/upcoming/free/"
    firfox_options = firfoxOptions()
    firfox_options.add_argument('--headless')
    browser = webdriver.Firefox(options=firfox_options)
    browser.get(url)
    wait = WebDriverWait(browser,60)
    wait.until(EC.presence_of_element_located((By.ID,"live-promotions")))
    return browser.page_source
def parse_page(html):
    games = []
    pattern = re.compile("<tr class=\"app sub\".*?appid=\"(\d+?)\" data-subid=\"(\d+?)\">.*?applogo\">.*?"
                         "<a href=\"(.+?)\">.*?<img.*?src=\"(.*?)\".*?>\s+</a>.*?<b>(.*?)</b>.*?"
                         "<td.*?(Keep|Weekend).*?</td>\s+<td.*?title=\"(.*?)\".*?title=\"(.*?)\".*?</tr>", re.S)
    items = re.findall(pattern,str(html))
    for item in items:
        game={}
        game["app_id"]=item[0]
        game['sub_id']=item[1]
        game['steam_link']="https://store.steampowered.com/app/" + item[0] + "/"
        game['img_link']=item[3]
        game['name']=item[4]
        game['type']=item[5]
        game['start_time'] = item[6].replace('–', '')
        game['end_time'] = item[7].replace('–', '')
        games.append(game)
    return games
def parse_games(games):
    game_list={
        "free_forever":[],
        "free_weekend":[],
        "type_unknow":[]
    }
    for game in games:
        if game['type']=="Keep":
            game_list['free_forever'].append(game)
        elif game['type']=="Weekend":
            game_list['free_weekend'].append(game)
        else:
            game_list['type_unknow'].append(game)

    return game_list

def make_report(game_list):
    report=""
    now_free="名称：{name}\n" \
             "免费类型：{freetype}\n" \
             "链接：{steam_link}\n" \
             "剩余时间：{left_time}\n" \
             "--------------------------\n"
    time_now=datetime.now(tz=timezone(timedelta(hours=8)))
    for game in game_list:
        start_time = parse(game['start_time'])
        end_time = parse(game['end_time'])
        if start_time <= time_now and end_time>time_now:
            temp_time= (end_time-time_now)
            left_days=temp_time.days
            left_hours=temp_time.seconds // 3600
            left_seconds=temp_time.seconds % 60
            left_time="{left_days}天{left_hours}小时{left_seconds}秒".format(left_days=left_days,left_hours=left_hours,left_seconds=left_seconds)
            if game['type'] == "Keep":
                freetype="永久免费"
            elif game['type'] == "Weekend":
                freetype="限时免费"
            else:
                freetype=""
            report += now_free.format(name=game['name'],freetype=freetype,steam_link=game['steam_link'],left_time=left_time)
    return report

def get_report(game_list,type :int=0):
    final_report=""
    if type == 0:
        for freetype in game_list:
            final_report += make_report(game_list[freetype])
        if not final_report.strip() :
            final_report="今天好像什么免费游戏都没有呢"
    elif type == 1:
        final_report += make_report(game_list['free_forever'])
        if not final_report.strip() :
            final_report += "今天好像没有永久免费游戏呢"
    elif type == 2:
        final_report += make_report(game_list['free_weekend'])
        if not final_report.strip() :
            final_report="今天好像没有限时免费游戏呢"
    return final_report.strip()

async def get_free_game(type:int=0):
    html=get_html()
    games=parse_page(html)
    game_list=parse_games(games)
    report= get_report(game_list,type)
    return report


if __name__ == '__main__':
    print(get_free_game())