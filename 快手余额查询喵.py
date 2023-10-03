"""
脚本作者: ❤❤❤❤❤不❤说❤❤❤❤
特别鸣谢: 偷CK的六舅哥提供的原始代码 
"""
import os
import sys
import time
import random
import requests
import re


def get_env(key):
    cookies = os.getenv(key)
    if cookies:
        # 使用多个分隔符：'\n', '@', 和 '&'
        return re.split('\n|@|&', cookies)
    else:
        print("===获取环境变量失败===")
        sys.stdout.flush()


def printf(text):
   
    print(f"[账号{i}]---{text}")
    sys.stdout.flush()

class KS:
    
    def __init__(self, cookie):
        cookie_list = cookie.strip().split("#")
        if len(cookie_list) >= 2:
            self.cookie = cookie_list[0]
            self.ua = cookie_list[1]
        else:
            print(f"【账号{i}】---Cookie格式不正确")

    def getname(self):
        try:
            url = f"https://nebula.kuaishou.com/rest/n/nebula/activity/earn/overview/basicInfo"
            headers = {
                "Host": "nebula.kuaishou.com",
                "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2012K11AC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.226 KsWebView/1.8.90.603 (rel) Mobile Safari/537.36 Yoda/3.1.2-rc1 ksNebula/11.4.10.5532 OS_PRO_BIT/64 MAX_PHY_MEM/11600 AZPREFIX/yz ICFO/0 StatusHT/36 TitleHT/43 NetType/WIFI ISLP/0 ISDM/0 ISLB/0 locale/zh-cn CT/0 ISLM/-1",
                "Cookie": self.cookie
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
        except Exception as e:
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
                "Cookie": self.cookie,
                "Connection": "keep-alive",
                "Accept": "*/*",
                "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2012K11AC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.226 KsWebView/1.8.90.603 (rel) Mobile Safari/537.36 Yoda/3.1.2-rc1 ksNebula/11.4.10.5532 OS_PRO_BIT/64 MAX_PHY_MEM/11600 AZPREFIX/yz ICFO/0 StatusHT/36 TitleHT/43 NetType/WIFI ISLP/0 ISDM/0 ISLB/0 locale/zh-cn CT/0 ISLM/-1",
                "Referer": "https://encourage.kuaishou.com/activity/qa?fid=2188974250&cc=panelPoster&followRefer=151&shareMethod=PICTURE&kpn=KUAISHOU&subBiz=QA_MAIN&shareToken=X-af3NYoEfqFI1WP&shareId=17568094332316&shareMode=APP&originShareId=17568094332316&layoutType=4&shareObjectId=2188974250&shareUrlOpened=0&timestamp=1691385657766",
                "Accept-Language": "zh-CN,zh-Hans;q=0.9",
                "Accept-Encoding": "gzip, deflate, br"
            }

            response = requests.request("GET", url=url, headers=headers, params=querystring)
            if response.status_code == 200:
                data = response.json().get('data', {})
                if response.json().get("result") == 1:
                    quiz_cash_amount = data.get('quizCashAmount', 0)
                    accumulative_withdraw_amount = data.get('accumulativeWithdrawAmount', 0)
                    return quiz_cash_amount, accumulative_withdraw_amount
                else:
                    return 0, 0
            else:
                print(f"Request failed with status code {response.status_code}")
                return 0, 0
        except Exception as e:
            print(f"获取余额失败: {e}")
            return 0, 0

    
    def run(self):
     
        name = self.getname()
        quiz_cash_amount, accumulative_withdraw_amount = self.select()

        formatted_quiz_cash = quiz_cash_amount / 10000
        formatted_withdraw_amount = accumulative_withdraw_amount / 100

        result = '✅' if quiz_cash_amount >= 360000 else '❌'
        print(f"【{i}】【{name}】【{formatted_withdraw_amount:.1f}】【{formatted_quiz_cash:.4f}】【{result}】")
        #print("【{:^2}】【{:^16}】【{:^2.1f}】【{:^2.4f}】【{:^5}】".format(i, name, formatted_withdraw_amount, formatted_quiz_cash, result))

if __name__ == "__main__":
    cookies = get_env("kuaishou_dt")
    print(f"【快手答题】共检测到{len(cookies)}个账号")
    print(f"==========================================")
    print(f"快手答题查询 by:❤❤❤❤")
    i = 1
    for cookie in cookies:
        KS(cookie).run()
        time.sleep(random.randint(5, 10))
        i += 1