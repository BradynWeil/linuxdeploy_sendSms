import json
import requests
import time

# 企业微信配置
from logger import LOGGER

AgentId = ""
CropId = ""
Secret = ""
Touser = ""
AccessToken = ""
RefreshTime = 0


# 刷新accestoken
def refreshAccesToken():
    try:
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (CropId, Secret)
        resp = requests.get(url)
        global AccessToken
        AccessToken = json.loads(resp.content.decode('utf-8'))["access_token"]
        global RefreshTime
        RefreshTime = int(time.time())
        LOGGER.info("获取accestoken成功")
    except:
        LOGGER.info("获取accestoken失败")
    return


def sendMessage(content):
    # 检查token是否失效
    checkAccessToken()
    try:
        while True:
            LOGGER.info("微信-开始发送信息")
            LOGGER.info(content)
            # sns = "FROM:" + content[0] + "\n" + content[1]
            url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % (AccessToken)
            body = {
                'touser': Touser,
                'msgtype': 'text',
                'agentid': AgentId,
                'text': {'content': content, },
                'safe': 0,
            }
            r = requests.post(url, data=json.dumps(body, ensure_ascii=False).encode('utf-8'))
            result = json.loads(r.content.decode('utf-8'))
            LOGGER.info(result['errcode'])
            if result['errcode'] == 40014 or result['errcode'] == 42001:
                LOGGER.info("TOKEN已过期，重新刷新")
                refreshAccesToken()
            if result['errcode'] == 0:
                # sqlObj.updateSmsById(str(_id))
                # del sqlObj
                LOGGER.info("微信-信息发送成功")
                return "Success"
                # break
    except Exception as e:
        LOGGER.info("微信-发送失败,异常:" + repr(e))
        return "Error"


def checkAccessToken():
    if RefreshTime == 0 or AccessToken == "":
        refreshAccesToken()
    if int(time.time()) - RefreshTime >= 7200:
        refreshAccesToken()
    return
