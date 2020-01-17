import json
import requests
import os

async def get_weather_of_city(city: str,date: int=0) -> str:
    citycode=getCityCode(city)
    if citycode:
        api = 'http://t.weather.sojson.com/api/weather/city/{}'.format(str(citycode))
        req = requests.get(api)
        weather = json.loads(req.text)
        today=['日期', '天气', '当前温度', '空气质量', '最高温', '最低温', '湿度', '风向', '风力', 'pm2.5', 'pm10', 'aqi', '日出', '日落', '注意事项']
        otherday = ['日期', '天气', '最高温', '最低温', '风向', '风力', 'aqi', '日出', '日落', '注意事项']

        base = {"日期": "{ymd}  {week}",
              "天气": "{type}",
              "当前温度": "{wendu}",
              "空气质量": "{quality}",
              "最高温": "{high}",
              "最低温": "{low}",
              "湿度": "{shidu}",
              "风向": "{fx}",
              "风力": "{fl}",
              "pm2.5": "{pm25}",
              "pm10": "{pm10}",
              "aqi": "{aqi}",
              "日出": "{sunrise}",
              "日落": "{sunset}",
              "注意事项": "{notice}"}

        info = {
            "wendu": weather['data']['wendu'],
            "shidu": weather['data']['shidu'],
            "quality": weather['data']['quality'],
            "pm25": weather['data']['pm25'],
            "pm10": weather['data']['pm10'],
            "ymd":weather['data']['forecast'][date]['ymd'],
            "week":weather['data']['forecast'][date]['week'],
            "type":weather['data']['forecast'][date]['type'],
            "high":weather['data']['forecast'][date]['high'],
            "low":weather['data']['forecast'][date]['low'],
            "fx":weather['data']['forecast'][date]['fx'],
            "fl":weather['data']['forecast'][date]['fl'],
            "aqi":weather['data']['forecast'][date]['aqi'],
            "sunrise":weather['data']['forecast'][date]['sunrise'],
            "sunset":weather['data']['forecast'][date]['sunset'],
            "notice":weather['data']['forecast'][date]['notice']
        }

        ans = ''
        if date == 0:
            for type in today:
                ans += type + ':' + base[type] + '\n'
        else:
            for type in otherday:
                ans += type + ':' + base[type] + '\n'
        ans = ans.format(**info).rstrip('\n')
        return ans
    else:
        return "抱歉没能查到这个城市呢"


def getCityCode(cityname:str):
    with open(os.path.dirname(__file__)  + "/citycode.json", "r")as fp:
        citycode = json.load(fp)
    for province in citycode['城市代码']:
        for city in province['市']:
            if cityname == city['市名']:
                return city['编码']

    return False

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True
