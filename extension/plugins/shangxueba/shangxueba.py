import requests
from .baiduapi import get_code
import json
import re
import os
import html2text
from bs4 import BeautifulSoup
from html import unescape


def set_cookie(session: requests.sessions.Session):
    if os.path.isfile("cookie.txt") and os.R_OK:
        with open("cookie.txt", "r") as fp:
            load_cookies = json.load(fp)
        session.cookies = requests.utils.cookiejar_from_dict(load_cookies)
    return session


def save_cookie(session: requests.sessions.Session):
    cookies = requests.utils.dict_from_cookiejar(session.cookies)
    with open("cookie.txt", "w") as fp:
        json.dump(cookies, fp)
    return cookies


def login(session: requests.sessions.Session):
    url="https://passport.shangxueba.com/user/userlogin.aspx?url=https%3A//www.shangxueba.com/"
    code_url="https://passport.shangxueba.com/VerifyCode.aspx"
    page=session.get(url)
    soup=BeautifulSoup(page.text,'lxml')
    #登录账号
    flag=False
    max_login_time=15
    while max_login_time > 0 and not flag:
        code_image=session.get(code_url).content
        with open("code.jpeg","wb") as f:
            f.write(code_image)
        code = get_code("./code.jpeg")
        headers={
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Referer":"https://passport.shangxueba.com/user/userlogin.aspx?url=https%3A//www.shangxueba.com/"
        }
        data={
            "__EVENTTARGET":"",
            "__EVENTARGUMENT":"",
            "__VIEWSTATE":soup.find('input', id='__VIEWSTATE')["value"],
            "__EVENTVALIDATION":soup.find('input', id='__EVENTVALIDATION')["value"],
            "txtName": "username",
            "txtPassword": "password",
            "txtVerifycode":code,
            "hidcode":"",
            "hidflag":"1",
            "Button1":""
        }
        req=session.post(url,headers=headers,data=data)
        if "欢迎您回来" in req.text:
            flag=True
            break
        if "验证码错误" in req.text:
            max_login_time -= 1
            continue
        else:
            max_login_time -= 1
            continue
    if flag == False:
        return False
    else:
        save_cookie(session)
        return session


def check_Login(session:requests.sessions.Session):
    html=session.get("http://passport.shangxueba.com").text
    pattern = re.compile("<p class=\"persPcConRiOneP2\">\s+\S+，欢迎您！</p>",re.S)
    if re.search(pattern, html):
        return True
    else:
        return False


def get_session_request():
    session=requests.session()
    session=set_cookie(session)
    if check_Login(session):
        return session
    else:
        session=login(session)
        if session:
            return session
    return False

def get_answer(session:requests.sessions.Session,queston_id:int):
    answer_url="http://www.shangxueba.com/ask/ajax/zuijiainfo.aspx?id={queston_id}".format(queston_id=queston_id)
    html = session.get(answer_url).text
    pattern = re.compile("<div class=\"xj_contextinfo\">\n<h6>\n(.*?)\n</h6>\n</div>", re.S)
    res = re.search(pattern, html)
    answer = html2text.html2text(res.group(1))
    return answer

def get_question(session:requests.sessions.Session,queston_id:int):
    question_url = "https://www.shangxueba.com/ask/{queston_id}.html".format(queston_id=queston_id)
    html = session.get(question_url).text
    pattern = re.compile("<div class=\"s_mess2_m\">(.*?)</div>", re.S)
    res = re.search(pattern, html)
    question = html2text.html2text(res.group(1))
    return question

async def get_answer_report(question_id):
    session=get_session_request()
    if not session:
        return "登录失败"
    question=get_question(session,question_id)
    answer=get_answer(session,question_id)
    report=question.strip() + "\n" + "--------------------------\n" + answer.strip()
    return report
def clean_html(html):
    html=unescape(html)
    html=html.replace("<br>","\n")
    return html
