import datetime
import requests
import json
import random
import time
import base64

import logging

from src.contant import USER_INFO, WECHAT_PUSH_KEY

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG)

MAP_URL = "https://apis.map.qq.com/ws/geocoder/v1/"

CHECK_REPEAT_CLOCK = "https://we.cqu.pt/api/mrdk/get_mrdk_flag.php"

HEALTHY_CLOCK = "https://we.cqu.pt/api/mrdk/post_mrdk_info.php"

WE_CHAT_PUSH = "https://sc.ftqq.com/" + WECHAT_PUSH_KEY + ".send"


def check_repeat_clock(user):
    key = {
        "xh": user[2],
        "timestamp": int(time.time())
    }
    res = base64.b64encode(json.dumps(key).encode('utf-8'))
    response = requests.post(url=CHECK_REPEAT_CLOCK, data={"key": res})
    print(response.text)
    return json.loads(response.text)['data']['count']


def we_chat_push(title, message):
    params = {"text": title, "desp": message}
    response = requests.get(url=WE_CHAT_PUSH, params=params)
    logging.info(json.loads(response.text)['errmsg'])


def clock():
    try:
        for user in USER_INFO:
            for i in range(10):
                if check_repeat_clock(user) is not "0":
                    logging.info(user[0] + "，已经打卡完成")
                    we_chat_push(user[0] + ", 重复打卡", "" + str(int(time.time())))
                    break
                key_map = {}
                address_map = address(user[3])
                province = address_map['address_components']['province']
                city = address_map['address_components']['city']
                district = address_map['address_components']['district']
                key_map['openid'] = user[4]
                key_map['name'] = user[0]
                key_map['xh'] = user[2]
                key_map['xb'] = user[1]
                key_map['locationBig'] = '中国,' + province + "," + city + "," + district
                key_map['locationSmall'] = city + district + address_map['title']
                key_map['latitude'] = str(address_map['location']['lat'])[0:-2] + str(my_random(10, 99))
                key_map['longitude'] = str(address_map['location']['lng'])[0:-2] + str(my_random(10, 99))
                key_map['szdq'] = province + "," + city + "," + district
                key_map['xxdz'] = user[3]
                key_map['ywjcqzbl'] = "低风险"
                key_map['ywjchblj'] = '无'
                key_map['xjzdywqzbl'] = '无'
                key_map['twsfzc'] = '是'
                key_map['ywytdzz'] = '无'
                key_map['beizhu'] = '无'
                key_map['timestamp'] = int(time.time())
                key_map['mrdkkey'] = get_mrdk_key(datetime.datetime.now().day, datetime.datetime.now().hour)
                res = str(base64.b64encode(json.dumps(key_map).encode('utf-8')))
                post_body = json.dumps({"key": res[2:-1]})
                headers = {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
                                  "Chrome/78.0.3904.62 XWEB/2693 MMWEBSDK/201001 Mobile Safari/537.36 MMWEBID/7311 "
                                  "MicroMessenger/7.0.20.1781(0x27001439) Process/appbrand2 WeChat/arm64 "
                                  "NetType/4G Language/zh_CN ABI/arm64",
                    'Content-Type': 'application/json',
                    "Referer": "https://servicewechat.com/wx8227f55dc4490f45/76/page-frame.html"
                }
                response = None
                try:
                    response = requests.post(url=HEALTHY_CLOCK, headers=headers, data=post_body)
                except Exception as e:
                    logging.error(e)

                if int(json.loads(response.text)['status']) == 200:
                    logging.info(response.text)
                    logging.info(user[0] + ", 打卡完成")
                    we_chat_push(user[0] + ",打卡成功", response.text + str(int(time.time())))
                    break
                else:
                    logging.error(user[0] + ", 打卡失败" + "," + response.text)
                    we_chat_push(user[0] + ",打卡失败", response.text + str(int(time.time())))
                    time.sleep(300)

    except Exception as e:
        logging.error(e)
        we_chat_push(e, "")


def my_random(min, max):
    return random.randint(min, max)


def address(addr):
    addr = {"address": addr, "key": "PULBZ-BSEWU-MAEVV-2IAJR-ZCAS3-53F4O"}
    response = json.loads(requests.get(url=MAP_URL, params=addr).text)
    print(response)
    return response['result']


def get_mrdk_key(day, hour):
    dateCode = [
        "s9ZS",
        "jQkB",
        "RuQM",
        "O0_L",
        "Buxf",
        "LepV",
        "Ec6w",
        "zPLD",
        "eZry",
        "QjBF",
        "XPB0",
        "zlTr",
        "YDr2",
        "Mfdu",
        "HSoi",
        "frhT",
        "GOdB",
        "AEN0",
        "zX0T",
        "wJg1",
        "fCmn",
        "SM3z",
        "2U5I",
        "LI3u",
        "3rAY",
        "aoa4",
        "Jf9u",
        "M69T",
        "XCea",
        "63gc",
        "6_Kf"
    ]

    hourCode = [
        "89KC",
        "pzTS",
        "wgte",
        "29_3",
        "GpdG",
        "FDYl",
        "vsE9",
        "SPJk",
        "_buC",
        "GPHN",
        "OKax",
        "_Kk4",
        "hYxa",
        "1BC5",
        "oBk_",
        "JgUW",
        "0CPR",
        "jlEh",
        "gBGg",
        "frS6",
        "4ads",
        "Iwfk",
        "TCgR",
        "wbjP"
    ]
    return dateCode[day] + hourCode[hour]