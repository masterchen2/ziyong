

import datetime
import os
import time
import random
import base64
import requests
import hashlib
import uuid
import json
import time
import requests
import random
import os
import json
import sys


now = str(round(time.time()*1000))
def ger_env(key):
    cookies = os.getenv(key)
    if cookies:
        cookies = cookies.split("&")
        return cookies
    else:
        print("===获取环境变量失败===")
        sys.stdout.flush()

def printf(text):
    print(f"[账号{i}]---{text}")
    sys.stdout.flush()


class KS:
    def __init__(self, cookie):
        cookie_list = cookie.split("#")
        self.cookie = cookie_list[0]
        self.ua = cookie_list[1]
        

    def run(self):

                 name = self.getname()
                 name2 = self.select()
                 name3 = name2 / 10000
                 print(f"【账户昵称】{name} 【答题余额】{name2}金币(约为{name3}元)")
                 if name2 >= 360000:
                       print(f"✅可以提现了")
                 else:
                      print(f"❌提现所需金币不够，还需要多答题哦~")

                 
    



   
           
             
    
            
    def getname(self):
     try:
        url = f"https://nebula.kuaishou.com/rest/n/nebula/activity/earn/overview/basicInfo"
        headers = {
    "Host": "nebula.kuaishou.com",
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2012K11AC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.226 KsWebView/1.8.90.603 (rel) Mobile Safari/537.36 Yoda/3.1.2-rc1 ksNebula/11.4.10.5532 OS_PRO_BIT/64 MAX_PHY_MEM/11600 AZPREFIX/yz ICFO/0 StatusHT/36 TitleHT/43 NetType/WIFI ISLP/0 ISDM/0 ISLB/0 locale/zh-cn CT/0 ISLM/-1",
    "Cookie": cookie
}
        response = requests.request("GET", url=url, headers=headers)
        if response.status_code == 200:
            if response.json().get("result") == 1:
                if response.json().get('data').get('userData').get('nickname') == "":
                     name = "ks"
                     return name
                else:
                     name = response.json().get('data').get('userData').get('nickname')
                     return name 
            else:
                name = "该用户未设置昵称"
                return name
     except:  
          name = "该用户未设置昵称" 
          return name   
            
    def select(self):
     try:
        url = f"https://encourage.kuaishou.com/rest/n/encourage/game/quiz/account/overview"
        querystring = {"wallet": "QA_CASH", "cursor": "",
                   "__NS_sig3": "e1f1b686915d0a5c37bd3abeb9b82529a9bdd5e81a4e29a3df53aeaea8a8abaa95b5",
                   "sigCatVer": "1"}
   
        headers = {
        "Host": "encourage.kuaishou.com",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Cookie": cookie,
        "Connection": "keep-alive",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2012K11AC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.226 KsWebView/1.8.90.603 (rel) Mobile Safari/537.36 Yoda/3.1.2-rc1 ksNebula/11.4.10.5532 OS_PRO_BIT/64 MAX_PHY_MEM/11600 AZPREFIX/yz ICFO/0 StatusHT/36 TitleHT/43 NetType/WIFI ISLP/0 ISDM/0 ISLB/0 locale/zh-cn CT/0 ISLM/-1",
        "Referer": "https://encourage.kuaishou.com/activity/qa?fid=2188974250&cc=panelPoster&followRefer=151&shareMethod=PICTURE&kpn=KUAISHOU&subBiz=QA_MAIN&shareToken=X-af3NYoEfqFI1WP&shareId=17568094332316&shareMode=APP&originShareId=17568094332316&layoutType=4&shareObjectId=2188974250&shareUrlOpened=0&timestamp=1691385657766",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept-Encoding": "gzip, deflate, br"
    }

        response = requests.request("GET", url=url, headers=headers, params=querystring)
        if response.status_code == 200:
            if response.json().get("result") == 1:
                name2 = response.json().get('data').get('quizCashAmount')
                return name2
            else:
                name2 = 0
                return name2
     except:  
          name2 = 0
          print(f"获取余额失败")
          return name2  

    

if __name__ == "__main__":
    cookies = ger_env("kuaishou_dt")
    print(f"【快手答题】共检测到{len(cookies)}个账号")
    print(f"==========================================")
    print(f"快手答题查询   by:偷CK的六舅哥\n10.1 bug提交 https://t.me/jiangyutck")
    i = 1
    for cookie in cookies:
        print(f"========【账号{i}】开始运行脚本========")
        i += 1
        KS(cookie).run()
        time.sleep(random.randint(5, 10))
        if i > len(cookies):
            break
        else:
            print("延迟一小会,准备跑下一个账号")