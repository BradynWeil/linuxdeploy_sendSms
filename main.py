import time
import sqlpy

# 数据库地址，记得必须挂载
# Dbpath = "/mnt/data/data/com.android.providers.telephony/databases/mmssms.db"
import wechat
from logger import LOGGER

Dbpath = "C:\\Users\\Bradyn\\Desktop\\mmssms.db"

# 通用配置
sim1 = "185*****967"
sim2 = ""  # 双卡卡2标识

# 发送设置
useWechat = True


def sendLoop():
    sqlObj = initSQL()
    # contents = sqlObj.readSmsById("687")
    # print(contents)
    # content = contents[0]
    # print(buildContentString(content[1], content[2], content[3], content[4]))
    # test.testsql("687",sqlObj)

    while True:
        LOGGER.info("开始读取短信消息")
        contents = sqlObj.readSms()
        if len(contents) != 0:
            LOGGER.info("发现{}条新消息".format(len(contents)))
            for content in contents:
                msg = ""
                if useWechat:
                    message = buildContentString(content[1], content[2], content[3], content[4])
                    msg.join(wechat.sendMessage(message))

                if "SUCCESS" in msg:
                    sqlObj.updateSmsById(str(content[0]))
        else:
            LOGGER.info("=============开始休眠================")
            time.sleep(5)
            # LOGGER.info("xiu")
    # del sqlObj


# 初始化数据库连接
def initSQL():
    LOGGER.info("数据库连接初始化")
    sqlObj = sqlpy.OperateSQL(Dbpath, LOGGER)
    return sqlObj


# 构建短信主体
def buildContentString(address, body, date, simId):
    if simId == 1:
        simName = sim1
    else:
        simName = sim2
    time_local = time.localtime(date / 1000)  # 去除毫秒
    template = '发信人：{}\n时间：{}\n短信内容：{}  【{}】'
    return template.format(address, time.strftime("%Y-%m-%d %H:%M:%S", time_local), body, simName)


sendLoop()
