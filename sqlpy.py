import sqlite3


class OperateSQL():
    def __init__(self, path, logger):
        self.path = path
        self.logger = logger

    def getConn(self):
        try:
            self.conn = sqlite3.connect(self.path)
        except sqlite3.Error as err:
            self.logger.info(err)
        return

    def updateSms(self):
        writeSql = "UPDATE sms SET seen = 1 ,read = 1 WHERE seen =0"  # 更改已经发送短信的读取状态
        try:
            self.getConn()
            cursor = self.conn.cursor()
            num = cursor.execute(writeSql)
            self.conn.commit()
            cursor.close()
            self.conn.close()
            return num

        except sqlite3.Error as err:
            self.logger.info(err)
            return 0
        finally:
            if self.conn:
                self.conn.close()

    def updateSmsById(self, id):
        writeSql = "UPDATE sms SET seen = 6 ,read = 1 WHERE _id = " + id  # 更改已经发送短信的读取状态
        print(writeSql)
        try:
            self.getConn()
            cursor = self.conn.cursor()
            num = cursor.execute(writeSql)
            self.conn.commit()
            cursor.close()
            self.conn.close()
            return num

        except sqlite3.Error as err:
            self.logger.info(err)
            return 0
        finally:
            if self.conn:
                self.conn.close()

    def readSms(self):
        readSql = "SELECT _id,address,body,date,sim_id FROM sms WHERE seen=0 And (Strftime('%s', 'now') - (date / 1000) <= 300)"  # 将未读取短信提取
        try:
            self.getConn()
            cursor = self.conn.cursor()
            cursor.execute(readSql)
            results = cursor.fetchall()
            self.conn.commit()
            cursor.close()
            self.conn.close()
            return results
        except sqlite3.Error as err:
            self.logger.info(err)
            return 0
        finally:
            if self.conn:
                self.conn.close()

    def readSmsById(self, id):
        readSql = "SELECT _id,address,body,date,sim_id FROM sms WHERE _id = " + id  # 将未读取短信提取
        try:
            self.getConn()
            cursor = self.conn.cursor()
            cursor.execute(readSql)
            results = cursor.fetchall()
            self.conn.commit()
            cursor.close()
            self.conn.close()
            return results
        except sqlite3.Error as err:
            self.logger.info(err)
            return 0
        finally:
            if self.conn:
                self.conn.close()
