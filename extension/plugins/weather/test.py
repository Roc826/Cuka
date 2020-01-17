import json
import time
info=[]
def getCityCode(cityname:str):
    with open("citycode.json", "r", encoding='utf-8')as fp:
        citycode = json.load(fp)
    for province in citycode['城市代码']:
        for city in province['市']:
            if cityname == city['市名']:
                return city['编码']

    return False
print(getCityCode("台州"))