import os
from aiohttp import web
from sqlFunction import *
from constValue import *
import aiohttp_jinja2
import copy

ROOT = os.path.dirname(__file__)


async def index(request):
    if 'userName' and 'password' in request.cookies:
        account = request.cookies['userName']
        password = request.cookies['password']
    else:
        account = ""
        password = ""
    response = aiohttp_jinja2.render_template("login.html", request, context={
        "account": account,
        "password": password
    })
    return response


async def register(request):
    # session = await get_session(request)
    content = open(os.path.join(ROOT, "template/register.html"), "r", encoding='UTF-8').read()
    return web.Response(content_type="text/html", text=content)


async def personHome(request):
    # print(help(request))
    # print(request.cookies)
    # session = await get_session(request)
    account, password = "", ""
    if 'userName' and 'password' in request.cookies:
        account = request.cookies['userName']
        password = request.cookies['password']
    else:
        return web.Response(status=400)

    now = datetime.datetime.now()
    sevenDay = datetime.timedelta(days=-7)
    before = now + sevenDay
    logs = selectChecksByRange(account, before.strftime('%Y-%m-%d'), now.strftime('%Y-%m-%d'))
    if not logs and logs != ():
        return web.Response(status=400)
    Logs = []
    for i in logs:
        t = copy.deepcopy(generalWeek_html)
        t = t.replace("#1", str(i[0]))
        t = t.replace("#2", str(i[1]))
        if i[2] == 0:
            t = t.replace("#3", "未签到")
        elif i[2] == 1:
            t = t.replace("#3", "已签到")
        elif i[2] == 2:
            t = t.replace("#3", "补签")
        elif i[2] == 3:
            t = t.replace("#3", "请假")
        else:
            t = t.replace("#3", "Unkonw")
        Logs.append(t)

    response = aiohttp_jinja2.render_template("employer-main.html", request, context={
        "logs": Logs,
    })
    return response


async def personCheck(request):
    status = ['签到', '签退']
    account, password = "", ""
    if 'userName' and 'password' in request.cookies:
        account = request.cookies['userName']
        password = request.cookies['password']
    else:
        return web.Response(status=400)

    checks = getPersonCheck(account, password)
    todayCheckSituation = []
    if checks == False:
        response = aiohttp_jinja2.render_template("personal-check.html", request,
                                                  context={'todayChech': todayCheckSituation})
        return response
    for i in range(len(checks)):
        t = copy.deepcopy(todayCheck)
        t = t.replace("#0", str(i))
        t = t.replace("#1", str(checks[i][0]))
        if checks[i][1] == 0:
            t = t.replace("#2", '未签到')
        elif checks[i][1] == 1:
            t = t.replace("#2", '已签到')
        elif checks[i][1] == 2:
            t = t.replace("#2", '补签')
        elif checks[i][1] == 3:
            t = t.replace("#2", '请假')
        else:
            t = t.replace("#2", 'Unkown')
        t = t.replace("#3", status[i % 2])

        todayCheckSituation.append(t)

    response = aiohttp_jinja2.render_template("personal-check.html", request,
                                              context={'todayChech': todayCheckSituation})
    return response


async def adminCheck(request):
    status = ['签到', '签退']
    account, password = "", ""
    if 'userName' and 'password' in request.cookies:
        account = request.cookies['userName']
        password = request.cookies['password']
    else:
        return web.Response(status=400)

    checks = getPersonCheck(account, password)
    todayCheckSituation = []
    if checks == False:
        response = aiohttp_jinja2.render_template("admin-check.html", request,
                                                  context={'todayChech': todayCheckSituation})
        return response
    for i in range(len(checks)):
        t = copy.deepcopy(todayCheck)
        t = t.replace("#0", str(i))
        t = t.replace("#1", str(checks[i][0]))
        if checks[i][1] == 0:
            t = t.replace("#2", '未签到')
        elif checks[i][1] == 1:
            t = t.replace("#2", '已签到')
        elif checks[i][1] == 2:
            t = t.replace("#2", '补签')
        elif checks[i][1] == 3:
            t = t.replace("#2", '请假')
        else:
            t = t.replace("#2", 'Unkown')
        t = t.replace("#3", status[i % 2])

        todayCheckSituation.append(t)

    response = aiohttp_jinja2.render_template("admin-check.html", request,
                                              context={'todayChech': todayCheckSituation})
    return response


# async def personApply(request):
#     account, password = "", ""
#     if 'userName' and 'password' in request.cookies:
#         account = request.cookies['userName']
#         password = request.cookies['password']
#     else:
#         return web.Response(status=400)
#
#     infoJson = {
#         'department': getPersonDepartment(account, password),
#     }
#     response = aiohttp_jinja2.render_template("pv-apply.html", request,
#                                               context=infoJson)
#     return response


async def personApply(request):
    if 'userName' and 'password' in request.cookies:
        account = request.cookies['userName']
        password = request.cookies['password']
    else:
        return web.Response(status=400)
    logInfo = getPersonApplylog(account, password)

    if logInfo == False:
        response = aiohttp_jinja2.render_template("personal-vocationmanage.html", request,
                                                  context={'logs': ""})
        return response
    strJ = ""
    for i in range(len(logInfo)):
        t = copy.deepcopy(applyLog_html)
        t = t.replace("#1", logInfo[i][0])

        if logInfo[i][1] == 0:
            t = t.replace("#2", '待审批')
        elif logInfo[i][1] == 1:
            t = t.replace("#2", '通过')
        elif logInfo[i][1] == 2:
            t = t.replace("#2", '未通过')
        elif logInfo[i][1] == 3:
            t = t.replace("#2", '已过期')

        t = t.replace("#3", str(logInfo[i][2]))
        t = t.replace("#4", str(logInfo[i][3]))
        t = t.replace("#5", str(logInfo[i][4]))
        strJ = strJ + t

    strJ = applyLog_html_before + strJ + applyLog_html_after
    department = getPersonDepartment(account, password)
    print(department)
    if not department:
        return web.Response(status=400)
    infoJson = {
        'logs': strJ,
        'department': department
    }
    response = aiohttp_jinja2.render_template("personal-vocationmanage.html", request,
                                              context=infoJson)
    return response


async def personInfo(request):
    # print(help(request))
    # print(request.cookies)
    # session = await get_session(request)
    account, password = "", ""
    if 'userName' and 'password' in request.cookies:
        account = request.cookies['userName']
        password = request.cookies['password']
    else:
        return web.Response(status=400)
    # content = open(os.path.join(ROOT, "template/main-personal.html"), "r", encoding='UTF-8').read()
    arr = getPersonInfo(account, password)
    if not arr:
        return web.Response(status=400)

    info = getPersonAllInfo(account, password)
    if not info:
        return web.Response(status=400)
    sex = "男"
    if str(info[2]) == "0":
        sex = "女"
    infoJson = {
        'id': str(info[0]),
        'name': info[1],
        'age': str(info[3]),
        'sex': sex,
        'department': info[4],
        'position': info[5],
        'phoneNumber': info[6],
        'avatar': arr[2],  # 头像
    }

    response = aiohttp_jinja2.render_template("main-personal.html", request, context=infoJson)
    return response

async def adminInfo(request):
    # print(help(request))
    # print(request.cookies)
    # session = await get_session(request)
    account, password = "", ""
    if 'userName' and 'password' in request.cookies:
        account = request.cookies['userName']
        password = request.cookies['password']
    else:
        return web.Response(status=400)
    # content = open(os.path.join(ROOT, "template/main-admin.html"), "r", encoding='UTF-8').read()
    arr = getPersonInfo(account, password)
    if not arr:
        return web.Response(status=400)

    info = getPersonAllInfo(account, password)
    if not info:
        return web.Response(status=400)
    sex = "男"
    if str(info[2]) == "0":
        sex = "女"
    infoJson = {
        'id': str(info[0]),
        'name': info[1],
        'age': str(info[3]),
        'sex': sex,
        'department': info[4],
        'position': info[5],
        'phoneNumber': info[6],
        'avatar': arr[2],  # 头像
    }

    response = aiohttp_jinja2.render_template("main-admin.html", request, context=infoJson)
    return response



# 人脸录入界面
async def personInput(request):
    account, password = "", ""
    if 'userName' and 'password' in request.cookies:
        account = request.cookies['userName']
        password = request.cookies['password']
    else:
        return web.Response(status=400)
    ok = getPersonName(account, password)
    if not ok and ok != ():
        return web.Response(status=400)
    response = aiohttp_jinja2.render_template("person-input.html", request,
                                              context={'name': ok})
    return response

async def admininput(request):
    account, password = "", ""
    if 'userName' and 'password' in request.cookies:
        account = request.cookies['userName']
        password = request.cookies['password']
    else:
        return web.Response(status=400)
    ok = getPersonName(account, password)
    if not ok and ok != ():
        return web.Response(status=400)
    response = aiohttp_jinja2.render_template("admin-input.html", request,
                                              context={'name': ok})
    return response



async def personSign(request):
    if 'userName' and 'password' in request.cookies:
        account = request.cookies['userName']
        password = request.cookies['password']
    else:
        return web.Response(status=400)

    ok = getPersonName(account, password)
    if not ok and ok != ():
        return web.Response(status=400)

    response = aiohttp_jinja2.render_template("person-sign.html", request,
                                              context={'name': ok})
    return response

async def adminsign(request):
    if 'userName' and 'password' in request.cookies:
        account = request.cookies['userName']
        password = request.cookies['password']
    else:
        return web.Response(status=400)
    
    # print(123)

    ok = getPersonName(account, password)
    if not ok and ok != ():
        return web.Response(status=400)

    # print(123)
    response = aiohttp_jinja2.render_template("admin-sign.html", request,
                                              context={'name': ok})
    return response


async def personOverview(request):
    account, password = "", ""
    if 'userName' and 'password' in request.cookies:
        account = request.cookies['userName']
        password = request.cookies['password']
    else:
        return web.Response(status=400)

    response = aiohttp_jinja2.render_template("pc-servey.html", request,
                                              context={})
    return response


async def adminHome(request):
    account, password = "", ""
    if 'userName' and 'password' in request.cookies:
        account = request.cookies['userName']
        password = request.cookies['password']
    else:
        return web.Response(status=400)

    r = userSelectLog(account, password)
    if r == False or r != "admin":
        return web.Response(status=400)

    arr = getPersonInfoAdmin(account)
    if not arr:
        return web.Response(status=400)

    department = getAdminDepartment(account)
    ok = getHomePendApply(department)
    if not ok and ok != ():
        return web.Response(status=400)

    pendApply = ""
    for i in range(len(ok)):
        t = copy.deepcopy(homePend_html)
        t = t.replace("#1", ok[i][0])
        t = t.replace("#2", ok[i][1])
        t = t.replace("#3", str(ok[i][2]))
        pendApply += t

    userInfoJson = {
        'name': arr[1],  # 姓名
        'identity': arr[0],  # 身份
        'avatar': arr[2],  # 头像
        'pendApply': pendApply
    }

    response = aiohttp_jinja2.render_template("admin-main.html", request,
                                              context=userInfoJson)
    return response


async def adminOA(request):
    if 'userName' and 'password' in request.cookies:
        account = request.cookies['userName']
        password = request.cookies['password']
    else:
        return web.Response(status=400)

    r = userSelectLog(account, password)
    if r == False or r != "admin":
        return web.Response(status=400)

    department = getAdminDepartment(account)
    ok = getPendApply(department)
    if not ok and ok != ():
        return web.Response(status=400)

    pendApply = []
    for i in range(len(ok)):
        t = copy.deepcopy(pendApply_html)
        t = t.replace("#1", ok[i][0])
        t = t.replace("#2", ok[i][1])
        t = t.replace("#3", str(ok[i][2]))
        t = t.replace("#4", str(ok[i][3]))
        t = t.replace("#5", str(ok[i][4]))
        pendApply.append(t)

    Logs = []
    logs = getFinApply(department)
    if not logs and logs != ():
        return web.Response(status=400)
    for i in range(len(logs)):
        t = copy.deepcopy(pendApply_html)
        t = t.replace("#1", logs[i][0])
        t = t.replace("#2", logs[i][1])
        t = t.replace("#3", str(logs[i][2]))
        t = t.replace("#4", str(logs[i][3]))
        t = t.replace("#5", str(logs[i][4]))
        Logs.append(t)

    response = aiohttp_jinja2.render_template("admin-vocationmanage.html", request,
                                              context={'pendApplys': pendApply, 'logs': Logs})
    return response


async def adminManage(request):
    if 'userName' and 'password' in request.cookies:
        account = request.cookies['userName']
        password = request.cookies['password']
    else:
        return web.Response(status=400)

    r = userSelectLog(account, password)
    if r == False or r != "admin":
        return web.Response(status=400)

    response = aiohttp_jinja2.render_template("admin-staffmanage.html", request,
                                              context={})
    return response


async def tableShowAdmin(request):
    data = request.rel_url.query
    name = data['name']
    applyTime = data['applyTime']

    detail = getDetailPendApply(name, applyTime)
    if not detail:
        return web.Response(status=400)
    infoJ = {
        'name': name,
        'applyTime': applyTime,
        'department': detail[0],
        'reason': detail[1],
        'startTime': str(detail[2]),
        'endTime': str(detail[3]),
    }

    response = aiohttp_jinja2.render_template("table-show.html", request,
                                              context=infoJ)
    return response


async def tableShow2Admin(request):
    data = request.rel_url.query
    name = data['name']
    applyTime = data['applyTime']
    detail = selectFinishApply(name, str(applyTime))
    if not detail:
        return web.Response(status=400)
    if str(detail[4]) == "1":
        status = "批准"
    elif str(detail[4]) == "2":
        status = "不批准"
    elif str(detail[4]) == "3":
        status = "过期"
    else:
        status = "UnKnown"
    infoJ = {
        'name': name,
        'applyTime': applyTime,
        'department': detail[0],
        'reason': detail[1],
        'startTime': str(detail[2]),
        'endTime': str(detail[3]),
        'sel': status,
        'adminReason': str(detail[5]),
    }

    response = aiohttp_jinja2.render_template("table-show2.html", request,
                                              context=infoJ)
    return response
