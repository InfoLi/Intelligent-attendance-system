import time
from logging import error
import pymysql
import traceback
import json
import datetime


conn = pymysql.connect(
    host="47.98.226.235",
    port=3306,
    user="softwave",
    password="softwave",
    db='softwave'
)


def allSign(cid, account, status,time, date):
    cursor = conn.cursor()
    sql = 'UPDATE userRollBook SET status = "' + status + '" ,time = "' + time +'" where account = "' + account + \
          '" and cid = "' + cid + '" and date = "' + date + '"'
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        if len(data) == 0:
            cursor.close()  # 关闭游标
            return True
        else:
            return False
    except:  # 返回None
        traceback.print_exc()
        print(conn.rollback())
        return False


def selectSignStatus(account, password):
    now = datetime.datetime.now()
    hour = int(now.strftime("%H"))
    checks = getPersonCheck(account, password)
    if not checks:
        return False
    if hour < 12 + 2:  # 下午两点 签上午的到or签退，需要先签退在签到
        if checks[0][1] == 0:
            # 签到
            if 0 < hour < 9:
                # 正常签到
                return allSign("1", account, "1", now.strftime("%H:%M:%S"),now.strftime("%Y-%m-%d"))
            else:
                return allSign("1", account, "2", now.strftime("%H:%M:%S"),now.strftime("%Y-%m-%d"))
        else:
            # 签退
            if hour < 12:
                # 早退
                return allSign("2", account, "2", now.strftime("%H:%M:%S"),now.strftime("%Y-%m-%d"))
            else:
                # 正常签退
                return allSign("2", account, "1", now.strftime("%H:%M:%S"),now.strftime("%Y-%m-%d"))
    else:
        if checks[2][1] == 0:
            # 签到
            if 13 < hour < 12 + 2:
                # 正常签到
                return allSign("3", account, "1", now.strftime("%H:%M:%S"),now.strftime("%Y-%m-%d"))
            else:
                return allSign("3", account, "2", now.strftime("%H:%M:%S"),now.strftime("%Y-%m-%d"))
        else:
            # 签退
            if hour < 12 + 6:
                # 早退
                return allSign("4", account, "2", now.strftime("%H:%M:%S"),now.strftime("%Y-%m-%d"))
            else:
                # 正常签退
                return allSign("4", account, "1", now.strftime("%H:%M:%S"),now.strftime("%Y-%m-%d"))



# 验证账号密码合法性
def userLog(userName, userPwd):
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    cursor = conn.cursor()
    sql = 'select passwd from userInfo where account = "' + str(userName) + '"'
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        if data[0][0] == str(userPwd):
            cursor.close()  # 关闭游标
            # conn.close()  # 关闭连接

            return True
        else:
            return False

    except:  # 返回None

        traceback.print_exc()
        print(conn.rollback())
        return False


# 登录分流
def userSelectLog(userName, userPwd):
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    cursor = conn.cursor()
    sql = 'select passwd from userInfo where account = "' + str(userName) + '"'
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        if data[0][0] == str(userPwd):
            sql = 'select permission from userInfo where account = "' + str(userName) + '"'
            try:
                cursor.execute(sql)
                conn.commit()
                data = cursor.fetchall()
                if data[0][0] is None:
                    cursor.close()  # 关闭游标
                    # conn.close()  # 关闭连接
                    return 'user'
                # 管理员
                elif data[0][0] == 'admin':
                    data = data[0][0]
                    return data


            except:  # 返回None
                traceback.print_exc()
                print(conn.rollback())
                return False
        else:
            return False

    except:  # 返回None

        traceback.print_exc()
        print(conn.rollback())
        return False


# 用户注册函数
def userRegister(Name, userName, userPwd, usersex, userage, userdepartment, userposition, userphone):
    """

    :param userName:
    :param userPwd:
    :param usersex:
    :param userage:
    :param userdepartment:
    :param userphone:
    :return:
    Ture:注册成功
    False:已注册
    """
    cursor = conn.cursor()
    content = [Name, userName, userPwd, usersex, userage, userdepartment, userposition, userphone]
    sql = "insert into userInfo(account,uname, passwd,sex,age,department,position,phone) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    # sql = "insert into userLR values (0,\"" + userName + "\",\"" + userPwd + "\",\"" + userPwd + "\",\"" + userPwd + "\",\"" + userPwd + "\",\"" + userPwd + "\",\"" + userPwd + "\");"
    try:
        cursor.executemany(sql, [content])
        # cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        if len(data) == 0:
            cursor.close()  # 关闭游标
            # conn.close()  # 关闭连接
            return True
        else:
            return False
    except:  # 返回None
        # 打印错误信息
        traceback.print_exc()
        conn.rollback()
        return False


# 上传头像（非人脸）
# 不能插入
def userInsertPhoto(Name, userPic):
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    cursor = conn.cursor()
    content = [Name, userPic]
    sql = "insert into userImg(account,img) values(%s,%s)"
    try:
        cursor.executemany(sql, [content])
        conn.commit()
        data = cursor.fetchall()
        if len(data) == 0:
            cursor.close()  # 关闭游标
            # conn.close()  # 关闭连接
            return True
        else:
            return False
    except:  # 返回None
        traceback.print_exc()
        print(conn.rollback())
        return False


# 获取个人头像
def getPersonInfo(userName, userPwd):
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    cursor = conn.cursor()
    if (userLog(userName, userPwd)):
        sql = 'select position,uname from userInfo where account = "' + str(userName) + '"'
        try:
            cursor.execute(sql)
            conn.commit()
            res = []
            data = cursor.fetchall()
            if len(data[0][0]) != 0:
                # cursor.close()  # 关闭游标
                # conn.close()  # 关闭连接
                res.append(data[0][0])
                res.append(data[0][1])
                sql2 = 'select img from userImg where account = "' + str(userName) + '"'
                try:
                    cursor.execute(sql2)
                    conn.commit()
                    data1 = cursor.fetchall()
                    if len(data1) != 0:
                        res.append(data1[0][0])
                        cursor.close()  # 关闭游标
                    else:
                        res.append("")
                        # print(res)
                        cursor.close()  # 关闭游标

                    return res
                except:
                    traceback.print_exc()
                    conn.rollback()
                    res.append('')
                    return res
            else:
                return False
        except:  # 返回None

            traceback.print_exc()
            print(conn.rollback())
            return False

# print(getPersonInfo('123','123'))
# 本日考勤记录
# 需要预先嵌入4条 暂定数据库完成操作
def getPersonCheck(userName, userPwd):
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    cursor = conn.cursor()
    if (userLog(userName, userPwd)):
        now = time.localtime()
        now_time = time.strftime("%Y-%m-%d", now)
        sql = 'select time,status from userRollBook where date=\"' + now_time + "\"" + 'and account=' + str(userName)
        try:
            cursor.execute(sql)
            conn.commit()
            res = []
            data = cursor.fetchall()
            if len(data) != 0:
                cursor.close()  # 关闭游标
                # conn.close()  # 关闭连接
                return data
            else:
                return False
        except:  # 返回None
            traceback.print_exc()
            conn.rollback()
            return False


def getPersonCheckSomeDay(userName, userPwd, now_time):
    cursor = conn.cursor()
    if (userLog(userName, userPwd)):
        sql = 'select time,status from userRollBook where date=\"' + now_time + "\"" + 'and account=' + str(userName)
        try:
            cursor.execute(sql)
            conn.commit()
            res = []
            data = cursor.fetchall()
            if len(data) != 0:
                cursor.close()  # 关闭游标
                # conn.close()  # 关闭连接
                return data
            else:
                return False
        except:  # 返回None
            traceback.print_exc()
            conn.rollback()
            return False



# 根据月份查询考勤记录
def selectChecksByMonth(account, Year, Month):
    cursor = conn.cursor()
    sql = 'select date,time,status from userRollBook where date >= "#1" and date <= "#2" and account="' + account + '"'
    date = Year + "-" + Month
    month = datetime.datetime.strptime(date, "%Y-%m").date()
    thirth = month+datetime.timedelta(days=30)
    sql = sql.replace("#1", str(month))
    sql = sql.replace("#2", str(thirth))
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        # print(data)
        return data
    except:  # 返回None
        traceback.print_exc()
        conn.rollback()
        return False

def selectIdNamePositionDe(account):
    cursor = conn.cursor()
    sql = 'select id,uname,position,department from userInfo where account = \"' + account + '\"'
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        return data
    except:  # 返回None
        traceback.print_exc()
        conn.rollback()
        return False
# print(getPersonCheck("123","123"))
# 获取个人部门信息
def getPersonDepartment(account, userPwd):
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    cursor = conn.cursor()
    if (userLog(account, userPwd)):
        # sql = 'select time,status from userRollBook where data='+str(now_time)+'and account='+str(userName)
        sql = 'select department from userInfo where account= "' + str(account) + '"'
        try:
            cursor.execute(sql)
            conn.commit()
            data = cursor.fetchall()
            # print(data)
            if len(data[0]) != 0:
                cursor.close()  # 关闭游标
                # conn.close()  # 关闭连接
                return data[0][0]
            else:
                return False
        except:  # 返回None
            traceback.print_exc()
            conn.rollback()
            return False


# print( getPersonDepartment("123","123"))
# 获取管理员部门信息
def getAdminDepartment(account):
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    cursor = conn.cursor()
    # sql = 'select time,status from userRollBook where data='+str(now_time)+'and account='+str(userName)
    sql = 'select department from userInfo where account= "' + str(account) + '"'
    try:
        cursor.execute(sql)
        conn.commit()

        data = cursor.fetchall()
        # print(data)
        if len(data[0]) != 0:

            cursor.close()  # 关闭游标
            # conn.close()  # 关闭连接
            return data[0][0]

        else:
            return False


    except:  # 返回None

        traceback.print_exc()
        conn.rollback()
        return False


# 查询个人的OA申请记录
def getPersonApplylog(account, userPwd):
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    cursor = conn.cursor()
    if (userLog(account, userPwd)):
        # sql = 'select time,status from userRollBook where data='+str(now_time)+'and account='+str(userName)
        sql = 'select name,status,startTime,endTime,applyTime from OA where account= "' + str(account) + '"'
        try:
            cursor.execute(sql)
            conn.commit()
            data = cursor.fetchall()
            return data
        except:  # 返回None
            traceback.print_exc()
            conn.rollback()
            return False


# print( getPersonApplylog("123","123"))
# 删除个人的申请
def deletePersonApplylog(account, userPwd, applyTime):
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    cursor = conn.cursor()
    if (userLog(account, userPwd)):
        # sql = 'select time,status from userRollBook where data='+str(now_time)+'and account='+str(userName)
        sql = 'delete from OA where applyTime=\"' + applyTime + "\"" + 'and account=' + str(account)
        try:
            cursor.execute(sql)
            conn.commit()
            data = cursor.fetchall()
            if len(data) == 0:
                cursor.close()  # 关闭游标
                # conn.close()  # 关闭连接
                return True
            else:
                return False
        except:  # 返回None
            traceback.print_exc()
            conn.rollback()
            return False


# print(deletePersonApplylog("123","123",'2022-07-03 11:37:18'))
# 获取员工名字
def getPersonName(account, userPwd):
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    cursor = conn.cursor()
    if (userLog(account, userPwd)):
        # sql = 'select time,status from userRollBook where data='+str(now_time)+'and account='+str(userName)
        sql = 'select uname from userInfo where account= "' + str(account) + '"'
        try:
            cursor.execute(sql)
            conn.commit()
            data = cursor.fetchall()
            # print(data)
            if len(data[0]) != 0:
                cursor.close()  # 关闭游标
                # conn.close()  # 关闭连接
                return data[0][0]
            else:
                return False
        except:  # 返回None
            traceback.print_exc()
            conn.rollback()
            return False


# print( getPersonName("123","123"))
# 提交OA申请
def userInsertOAApply(account, userPwd, starttime, endtime, reason, department):
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    name = getPersonName(account, userPwd)
    now = time.localtime()
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
    cursor = conn.cursor()
    content = [account, name, now_time, starttime, endtime, reason, department, '0']
    sql = "insert into OA(account,name,applyTime,startTime,endTime,reason,department,status) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
        cursor.executemany(sql, [content])
        conn.commit()
        data = cursor.fetchall()
        if len(data) == 0:
            cursor.close()  # 关闭游标
            # conn.close()  # 关闭连接
            return True
        else:
            return False
    except:  # 返回None
        traceback.print_exc()
        conn.rollback()
        return False


# print(userInsertOAApply(123,123,"2022-07-01","2022-07-02",'打爆king'))
# 获取个人的全部信息
def getPersonAllInfo(userName, userPwd):
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    cursor = conn.cursor()
    if (userLog(userName, userPwd)):
        now = time.localtime()
        # sql = 'select time,status from userRollBook where data='+str(now_time)+'and account='+str(userName)
        sql = 'select id,uname,sex,age,department,position,phone from userInfo where account= "' + str(userName) + '"'
        try:
            cursor.execute(sql)
            conn.commit()
            data = cursor.fetchall()
            # print(data)
            if len(data[0]) != 0:
                cursor.close()  # 关闭游标
                # conn.close()  # 关闭连接
                return data[0]
            else:
                return False
        except:  # 返回None
            traceback.print_exc()
            conn.rollback()
            return False


# print(getPersonAllInfo("123","123"))
# 更新个人信息
def updataPersonAllInfo(userName, userPwd, name, age, sex, deapartment, position, phoneNum):
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    cursor = conn.cursor()
    if (userLog(userName, userPwd)):
        now = time.localtime()
        # sql = 'select time,status from userRollBook where data='+str(now_time)+'and account='+str(userName)
        sql = 'UPDATE userInfo SET uname =\"' + str(name) + '\" , age =\"' + str(age) + '\" , sex =\"' + str(
            sex) + '\", department =\"' + str(deapartment) + '\", position =\"' + str(position) + '\", phone =\"' + str(
            phoneNum) + '\"  WHERE account =' + str(userName)
        # sql = 'UPDATE userInfo SET uname =\"'+str(name)+'\"  WHERE account ='+ str(userName)
        # select id,uname,sex,age,department,position,phone from userInfo where account=' + str(userName)
        try:
            cursor.execute(sql)
            conn.commit()
            data = cursor.fetchall()
            # print(data)
            if len(data) == 0:
                cursor.close()  # 关闭游标
                # conn.close()  # 关闭连接
                return True
            else:
                return False
        except:  # 返回None
            traceback.print_exc()
            conn.rollback()
            return False


# 获取管理管理员姓名和职位
def getPersonInfoAdmin(userName):
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    cursor = conn.cursor()
    sql = 'select position,uname from userInfo where account = "' + str(userName) + '"'
    try:
        cursor.execute(sql)
        conn.commit()
        res = []
        data = cursor.fetchall()
        if len(data[0][0]) != 0:
            # cursor.close()  # 关闭游标
            # conn.close()  # 关闭连接
            res.append(data[0][0])
            res.append(data[0][1])
            sql2 = 'select img from userImg where account = ' + str(userName)
            try:
                cursor.execute(sql2)
                conn.commit()
                data1 = cursor.fetchall()
                if len(data1[0]) != 0:
                    res.append(data1[0][0])
                    cursor.close()  # 关闭游标
                    # conn.close()  # 关闭连接
                    return res
                else:
                    return False
            except:
                traceback.print_exc()
                conn.rollback()
                res.append('')
                return res
        else:
            return False
    except:  # 返回None
        traceback.print_exc()
        print(conn.rollback())
        return False


def getPendApply(department):
    cursor = conn.cursor()
    sql = 'select name,department,startTime,endTime,applyTime from OA where status = \"' + str(
        0) + '\" and department = \"' + department + '\"'
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        return data
    except:  # 返回None
        traceback.print_exc()
        print(conn.rollback())
        return False


def getHomePendApply(department):
    cursor = conn.cursor()
    sql = 'select account,name,reason from OA where status = \"' + str(
        0) + '\" and department = \"' + department + '\"'
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        return data
    except:  # 返回None
        traceback.print_exc()
        print(conn.rollback())
        return False

def getFinApply(department):
    cursor = conn.cursor()
    sql = 'select name,department,startTime,endTime,applyTime from OA where status != \"' + str(
        0) + '\" and department = \"' + department + '\"'
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()

        return data
    except:  # 返回None
        traceback.print_exc()
        print(conn.rollback())
        return False


# print(getPendApply('财务部'))
# 获取同部门待审批OA
def getDetailPendApply(name, applyTime):
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    cursor = conn.cursor()
    sql = 'select department,reason,startTime,endTime from OA where name = \"' + str(name) + '\" and applyTime = \"' + applyTime + '\"'
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        if len(data) != 0:
            cursor.close()  # 关闭游标
            # conn.close()  # 关闭连接
            return data[0]
        else:
            return False
    except:  # 返回None
        traceback.print_exc()
        print(conn.rollback())
        return False


# print(getDetailPendApply('ljz','2022-07-03 22:02:59'))

def insertInputFace(account, imgPresentation):
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    cursor = conn.cursor()
    sql = "insert into userFaceData values(" + account + ",\"" + imgPresentation + "\")"
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        if len(data) == 0:
            cursor.close()  # 关闭游标
            # conn.close()  # 关闭连接
            return True
        else:
            return False
    except:  # 返回None
        traceback.print_exc()
        conn.rollback()
        return False


def getAllFaces():
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    cursor = conn.cursor()
    sql = 'select json_extract(data,"$[*]") d from userFaceData'
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        return data
    except:  # 返回None
        traceback.print_exc()
        conn.rollback()
        return False


def getAllIden():
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    cursor = conn.cursor()
    sql = 'select account from userFaceData'
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        return data
    except:  # 返回None
        traceback.print_exc()
        conn.rollback()
        return False

# 根据范围查询考勤记录
def selectChecksByRange(account, startTime, endTime):
    cursor = conn.cursor()
    sql = 'select date,time,status from userRollBook where date >= "#1" and date <= "#2" and account="' + account + '"'
    sql = sql.replace("#1", startTime)
    sql = sql.replace("#2", endTime)
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        return data
    except:  # 返回None
        traceback.print_exc()
        conn.rollback()
        return False

# 根据范围查询考勤记录
def selectChecksByRangeA(department, startTime, endTime):
    cursor = conn.cursor()
    sql = 'select date,time,status from userRollBook where date >= "#1" and date <= "#2" and department="' + department + '"'
    sql = sql.replace("#1", startTime)
    sql = sql.replace("#2", endTime)
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        return data
    except:  # 返回None
        traceback.print_exc()
        conn.rollback()
        return False


def selectFinishApply(name, applyTime):
    """
    :param userName:
    :param userPwd:
    :return:
    Ture:登陆成功
    Flase:登录失败
    """
    cursor = conn.cursor()

    sql = 'select department,reason,startTime,endTime,' \
          'status,adminReason from OA where name=\"' + name + '\" and applyTime = "' + applyTime +'"'
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        print(data)
        if len(data) != 0:
            cursor.close()  # 关闭游标
            # conn.close()  # 关闭连接
            return data[0]
        else:
            return False

    except:  # 返回None
        traceback.print_exc()
        print(conn.rollback())
        return False



# 管理员提交审批
def changePendApply(adminaccount, applyTime, username, selApproval, remarks):

    now = time.localtime()
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
    cursor = conn.cursor()
    sql = 'select uname from userInfo where account = ' + str(adminaccount)
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        # print(data)
        if len(data) != 0:
            sql = 'UPDATE OA SET approvalTime =\"' + str(now_time) + '\" , status =\"' + str(
                selApproval) + '\" , adminReason =\"' + str(remarks) + '\" , adminName =\"' + str(
                data[0][0]) + '\"  WHERE applyTime =\"' + str(applyTime) + '\" and name =\"' + str(username) + '\"'
            try:
                cursor.execute(sql)
                conn.commit()
                data = cursor.fetchall()
                if len(data) == 0:
                    cursor.close()  # 关闭游标
                    # conn.close()  # 关闭连接
                    return True
                else:
                    return False
            except:  # 返回None
                traceback.print_exc()
                print(conn.rollback())
                return False
        else:
            return False
    except:  # 返回None
        traceback.print_exc()
        print(conn.rollback())
        return False

def selectInfoByType(type_, ran):
    cursor = conn.cursor()
    if type_ == "id":
        sql = 'select id, uname,sex, position,department from userInfo where id= \"' + ran + '\"'
    elif type_ == "name":
        sql = 'select id, uname, sex,position,department from userInfo where uname= \"' + ran + '\"'
    elif type_ == "position":
        sql = 'select id, uname,sex, position,department from userInfo where position= \"' + ran + '\"'
    elif ran == "":
        sql = 'select id, uname, sex,position,department from userInfo'
    else:
        sql = 'select id, uname,sex, position,department from userInfo'
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        # print(data)
        return data
    except:  # 返回None
        traceback.print_exc()
        conn.rollback()
        return False




