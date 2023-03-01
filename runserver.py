import argparse
import asyncio
import base64
import copy
import json
import logging
import os
import platform
import ssl
import time
import numpy as np
from aiohttp_session import setup, get_session, SimpleCookieStorage
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import cv2
from cryptography import fernet
import jinja2
from aiohttp import web
import aiohttp_jinja2
from sqlFunction import *
from constValue import *
from routerGet import *
from onnxServer import *

from aiortc import (
    MediaStreamTrack,
    RTCDataChannel,
    RTCPeerConnection,
    RTCSessionDescription,
    VideoStreamTrack,
)
from aiortc.contrib.media import MediaPlayer, MediaRelay

# from av import VideoFrame

ROOT = os.path.dirname(__file__)

global imgPresentations
global distances
global identity

relay = None
webcam = None


def decodeBase64Img(img_uri):
    """
    根据base64生成图片
    :img_path:生成的图片路径
    :img_uri:图片的base64 uri
    """
    try:
        # 截取uri的data:image/png;base64后端的uri
        img_uri = img_uri.split(",")[1]
        imgdata = base64.b64decode(img_uri)
        return imgdata
    except:
        traceback.print_exc()


async def receive(request):
    content = open(os.path.join(ROOT, "static/index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)


async def meet(request):
    content = open(os.path.join(ROOT, "template/personal-meeting.html"), "r", encoding='utf-8').read()
    return web.Response(content_type="text/html", text=content)

async def meet2(request):
    content = open(os.path.join(ROOT, "template/admin-meeting.html"), "r", encoding='utf-8').read()
    return web.Response(content_type="text/html", text=content)

async def test(request):
    # params = await request.get()
    # print(params)
    context = {'values': [1, 2, 3, 4], 'squares': [4, 3, 2, 1], 'order': "<h2>1123456</h2>"}
    response = aiohttp_jinja2.render_template("test.html", request, context)
    return response


async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
    pc = RTCPeerConnection()
    pcs.add(pc)

    account = ""
    if 'account' and 'password' in request.cookies:
        account = request.cookies['userName']
    else:
        return web.Response(status=400)

    if 1 not in app['meeting']:
        app['meeting'][1] = []
        app['meeting'][1].append(account)
    else:
        app['meeting'][1].append(account)

    print(app['meeting'])
    await server(pc, offer, account)

    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )


pcs = set()


async def server(pc, offer, userName):
    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            # 结束视频会议
            if app['meeting'] == userName:
                # 全部结束
                app['meeting'][1] = []
                for i in pcs:
                    await i.close()
                    pcs.discard(i)
            else:
                await pc.close()
                pcs.discard(pc)

    @pc.on("track")
    def on_track(track):
        print("======= received track: ", track)
        print(track.kind)
        if track.kind == "video":
            t = VideoTalk(track, userName)
            pc.addTrack(t)
        elif track.kind == "audio":
            t = AudioTalk(track, userName)
            pc.addTrack(t)

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)


async def on_shutdown(app):
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()


class VideoTalk(VideoStreamTrack):
    kind = "video"

    def __init__(self, track, userName):
        super().__init__()
        self.track = track
        self.userName = userName

    async def recv(self):
        global f
        if self.userName == app['meeting'][1][0]:
            timestamp, video_timestamp_base = await self.next_timestamp()
            frame = await self.track.recv()
            frame.pts = timestamp
            frame.time_base = video_timestamp_base
            f = frame
            return frame
        else:
            return f


class AudioTalk(VideoStreamTrack):
    kind = "audio"

    def __init__(self, track, userName):
        super().__init__()
        self.track = track
        self.userName = userName

    async def recv(self):
        global a
        # timestamp, video_timestamp_base = await self.next_timestamp()
        # audio.pts = timestamp
        # audio.time_base = video_timestamp_base

        if self.userName == app['meeting'][1][0]:
            audio = await self.track.recv()
            # print("audio")
            a = audio
            return audio
        else:
            return a


async def deal(request):
    data = await request.post()
    method = data['method']
    if method == 'register':
        # session = await get_session(request)
        Name = data["Name"]  # 账号
        userName = data['userName']  # 姓名
        password = data['password']
        userSex = data['userSex']
        userRge = data['userRge']
        userDepartment = data['userDepartment']
        userPosition = data['userPosition']
        userPhone = data['userPhone']
        ok = userRegister(Name, userName, password, userSex, userRge, userDepartment, userPosition, userPhone)
        if ok:
            response = web.Response(status=200, content_type="text/html", text="yes")
            response.set_cookie("userName", Name)
            response.set_cookie("password", password)
            return response
        else:
            return web.Response(status=400, content_type="text/html", text="注册失败")
    elif method == 'login':
        username = data['username']
        password = data['password']
        ok = userSelectLog(username, password)
        if not ok:
            return web.Response(status=400, content_type="text/html", text="登录失败")

        else:
            response = web.Response(status=200, content_type="text/html", text=ok)
            response.set_cookie("userName", username, max_age=3600 * 12)
            response.set_cookie("password", password, max_age=3600 * 12)
            return response
    elif method == 'insertPhoto':
        name = request.cookies['userName']
        file = data['file'].file
        byte_img = base64.b64encode(file.read())
        image = byte_img.decode('utf-8')
        image = "data:image/png;base64," + image
        ok = userInsertPhoto(name, image)
        if ok:
            response = web.Response(status=200, content_type="text/html", text="yes")
            return response
        else:
            return web.Response(status=400, content_type="text/html", text="登录失败")
    elif method == 'apply':
        account, password = "", ""
        if 'userName' and 'password' in request.cookies:
            account = request.cookies['userName']
            password = request.cookies['password']
        else:
            return web.Response(status=400)
        # print(data)
        startTime = data['starttime']
        endTime = data['endtime']
        reason = data['reason']
        department = data['department']
        if userInsertOAApply(account, password, startTime, endTime, reason, department):
            return web.Response(status=200, content_type="text/html", text="yes")
        else:
            return web.Response(status=400)
    elif method == 'cancelApply':
        account, password = "", ""
        if 'userName' and 'password' in request.cookies:
            account = request.cookies['userName']
            password = request.cookies['password']
        else:
            return web.Response(status=400)
        canselApplyTime = data['canselApplyTime']
        if deletePersonApplylog(account, password, canselApplyTime):
            return web.Response(status=200, content_type="text/html", text="yes")
        else:
            return web.Response(status=400)
    elif method == 'changeBasicInfo':
        account, password = "", ""
        if 'userName' and 'password' in request.cookies:
            account = request.cookies['userName']
            password = request.cookies['password']
        else:
            return web.Response(status=400)
        name = data['name']
        age = data['age']
        sex = data['sex']
        deapartment = data['apartment']
        position = data['position']
        phoneNum = data['pnum']
        if updataPersonAllInfo(account, password, name, age, sex, deapartment, position, phoneNum):
            return web.Response(status=200, content_type="text/html", text="yes")
        else:
            return web.Response(status=400)
    elif method == "inputFace":
        account, password = "", ""
        if 'userName' and 'password' in request.cookies:
            account = request.cookies['userName']
            password = request.cookies['password']
        else:
            return web.Response(status=400)

        byte_img = data['img']
        byte_img = decodeBase64Img(byte_img)
        encode_image = np.asarray(bytearray(byte_img), dtype="uint8")  # 二进制转换为一维数组
        img_array = cv2.imdecode(encode_image, cv2.IMREAD_COLOR)  # 用cv2解码为三通道矩阵
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)  # BGR2RGB

        faces = run_onnx_extract_faces(img_array)
        if len(faces) == 0:
            return web.Response(status=400, content_type="text/html", text="不存在人脸")
        elif len(faces) >= 2:
            return web.Response(status=400, content_type="text/html", text="人脸大于1")
        imgPresentation = run_onnx_presentation(faces[0])

        if insertInputFace(account, str(imgPresentation)):
            return web.Response(status=200, content_type="text/html", text="ok")
        else:
            return web.Response(status=400, content_type="text/html", text="fail")
    elif method == "sign":
        if 'userName' and 'password' in request.cookies:
            account = request.cookies['userName']
            password = request.cookies['password']
        else:
            return web.Response(status=400)
        byte_img = data['img']
        byte_img = decodeBase64Img(byte_img)
        encode_image = np.asarray(bytearray(byte_img), dtype="uint8")  # 二进制转换为一维数组
        img_array = cv2.imdecode(encode_image, cv2.IMREAD_COLOR)  # 用cv2解码为三通道矩阵
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)  # BGR2RGB

        faces = run_onnx_extract_faces(img_array)
        if len(faces) == 0:
            return web.Response(status=400, content_type="text/html", text="不存在人脸")
        elif len(faces) >= 2:
            return web.Response(status=400, content_type="text/html", text="人脸大于1")
        imgPresentation = run_onnx_presentation(faces[0])
        imgPresentation = np.array(imgPresentation)
        # print(np.dot(imgPresentation, imgPresentations.T))
        similar = np.dot(imgPresentation, imgPresentations.T) \
                  / (np.sqrt(np.sum(np.multiply(imgPresentation, imgPresentation))) * distances)

        maxSim = np.max(similar)
        if maxSim < 0.4:
            return web.Response(status=400, content_type="text/html", text="人脸识别失败")
        maxSimPosition = np.where(similar == maxSim)

        if account == identity[maxSimPosition[0][0]]:
            if not selectSignStatus(account, password):
                return web.Response(status=400, content_type="text/html", text="签到失败")

        return web.Response(status=200, content_type="text/html", text="ok")
    elif method == "queryCheckDay":
        account, password = "", ""
        if 'userName' and 'password' in request.cookies:
            account = request.cookies['userName']
            password = request.cookies['password']
        else:
            return web.Response(status=400, content_type="text/html", text="fail")

        queryDay = data['queryDay']
        checks = getPersonCheckSomeDay(account, password, queryDay)

        dayCheckSit = []
        for i in range(len(checks)):
            t = str(checks[i][0])
            if checks[i][1] == 0:
                t += '未签到'
            elif checks[i][1] == 1:
                t += '已签到'
            elif checks[i][1] == 2:
                t += '补签'
            elif checks[i][1] == 3:
                t += '请假'
            else:
                t += 'Unkown'

            dayCheckSit.append(t)

        return web.json_response({'days': dayCheckSit}, status=200)
    elif method == "approve":
        if 'userName' and 'password' in request.cookies:
            account = request.cookies['userName']
            password = request.cookies['password']
        else:
            return web.Response(status=400)

        r = userSelectLog(account, password)
        if r == False or r != "admin":
            return web.Response(status=400)
        applyTime = data['applyTime']
        name = data['name']
        remarks = data['remarks']
        selApproval = data['sel']
        ok = changePendApply(account, applyTime, name, selApproval, remarks)
        if not ok:
            return web.Response(status=400)
        # 修改考勤信息？
        return web.Response(status=200, content_type="text/html", text="ok")
    elif method == "searchMonth":
        if 'userName' and 'password' in request.cookies:
            account = request.cookies['userName']
            password = request.cookies['password']
        else:
            return web.Response(status=400)

        year = data['year']
        month = data['month']
        ok = selectChecksByMonth(account, str(year), str(month))
        if not ok and ok != ():
            return web.Response(status=400)

        info = selectIdNamePositionDe(account)[0]

        str_ = ""
        for i in range(len(ok)):
            t = copy.deepcopy(personMonth_html)
            t = t.replace("#1", str(info[0]))
            t = t.replace("#2", info[1])
            t = t.replace("#3", info[2])
            t = t.replace("#4", info[3])
            t = t.replace("#4", info[3])
            t = t.replace("#5", str(ok[i][0]))
            t = t.replace("#6", str(ok[i][1]))
            if str(ok[i][2]) == "0":
                status = "未签到"
            elif str(ok[i][2]) == "1":
                status = "已签到"
            elif str(ok[i][2]) == "2":
                status = "补签"
            else:
                status = "Unknown"
            t = t.replace("#7", status)
            str_ += t
            if i != len(ok) - 1:
                str_ += ","

        return web.Response(status=200, content_type="text/html",
                            text='[' + str_ + ']')
    elif method == "searchRange":
        if 'userName' and 'password' in request.cookies:
            account = request.cookies['userName']
            password = request.cookies['password']
        else:
            return web.Response(status=400)

        startTime = data['year1'] + '-' + data['month1'] + '-' + data['day1']
        endTime = data['year2'] + '-' + data['month2'] + '-' + data['day2']

        ok = selectChecksByRange(account, startTime, endTime)
        if not ok and ok != ():
            return web.Response(status=400)

        info = selectIdNamePositionDe(account)[0]

        str_ = ""
        for i in range(len(ok)):
            t = copy.deepcopy(personRange_html)
            t = t.replace("#1", str(info[0]))
            t = t.replace("#2", info[1])
            t = t.replace("#3", info[2])
            t = t.replace("#4", info[3])
            t = t.replace("#4", info[3])
            t = t.replace("#5", str(ok[i][0]))
            t = t.replace("#6", str(ok[i][1]))
            if str(ok[i][2]) == "0":
                status = "未签到"
            elif str(ok[i][2]) == "1":
                status = "已签到"
            elif str(ok[i][2]) == "2":
                status = "补签"
            else:
                status = "Unknown"
            t = t.replace("#7", '"' + status)
            str_ += t
            if i != len(ok) - 1:
                str_ += ","
        return web.Response(status=200, content_type="text/html",
                            text='[' + str_ + ']')
    elif method == "adminRegister":
        if 'userName' and 'password' in request.cookies:
            account = request.cookies['userName']
        else:
            return web.Response(status=400)

        userDepartment = getAdminDepartment(account)
        account = data["Name"]  # 账号
        userName = data['userName']  # 姓名
        password = data['password']
        if data['userSex'] == '男':
            userSex = "1"
        else:
            userSex = "0"
        userRge = data['userRge']
        # userDepartment = data['userDepartment']
        userPosition = data['userPosition']
        userPhone = data['userPhone']

        ok = userRegister(account, userName, password, userSex, userRge, userDepartment, userPosition, userPhone)
        if ok:
            response = web.Response(status=200, content_type="text/html", text="ok")
            return response
        else:
            return web.Response(status=400, content_type="text/html", text="注册失败")
    elif method == "searchInfo":
        if 'userName' and 'password' in request.cookies:
            account = request.cookies['userName']
            password = request.cookies['password']
        else:
            return web.Response(status=400, content_type="text/html", text="fail")

        r = userSelectLog(account, password)
        if r == False or r != "admin":
            return web.Response(status=400, content_type="text/html", text="fail")
        searchtype = data['searchtype']
        searchcontent = data['searchcontent']

        ok = selectInfoByType(searchtype, searchcontent)
        if not ok:
            return web.Response(status=400, content_type="text/html", text="fail")

        str_ = ""
        for i in range(len(ok)):
            t = copy.deepcopy(adminSearch_html)
            t = t.replace("#1", str(ok[i][0]))
            t = t.replace("#2", ok[i][1])
            if str(ok[i][2]) == "1":
                sex = "男"
            else:
                sex = "女"
            t = t.replace("#3", sex)
            t = t.replace("#4", ok[i][3])
            t = t.replace("#5", ok[i][4])
            str_ += t
            if i != len(ok) - 1:
                str_ += ","
        return web.Response(status=200, content_type="text/html", text='[' + str_ + ']')
    elif method == "searchRangeA":
        if 'userName' and 'password' in request.cookies:
            account = request.cookies['userName']
            password = request.cookies['password']
        else:
            return web.Response(status=400)

        startTime = data['year1'] + '-' + data['month1'] + '-' + data['day1']
        endTime = data['year2'] + '-' + data['month2'] + '-' + data['day2']

        de = getAdminDepartment(account)
        if not de and de != ():
            return web.Response(status=400)

        ok = selectChecksByRangeA(de, startTime, endTime)
        if not ok and ok != ():
            return web.Response(status=400)

        info = selectIdNamePositionDe(account)[0]

        str_ = ""
        for i in range(len(ok)):
            t = copy.deepcopy(personRange_html)
            t = t.replace("#1", str(info[0]))
            t = t.replace("#2", info[1])
            t = t.replace("#3", info[2])
            t = t.replace("#4", info[3])
            t = t.replace("#4", info[3])
            t = t.replace("#5", str(ok[i][0]))
            t = t.replace("#6", str(ok[i][1]))
            if str(ok[i][2]) == "0":
                status = "未签到"
            elif str(ok[i][2]) == "1":
                status = "已签到"
            elif str(ok[i][2]) == "2":
                status = "补签"
            else:
                status = "Unknown"
            t = t.replace("#7", '"' + status)
            str_ += t
            if i != len(ok) - 1:
                str_ += ","
        return web.Response(status=200, content_type="text/html",
                            text='[' + str_ + ']')
    else:
        return web.Response(status=400, content_type="text/html", text="错误方法")

    # return web.Response(content_type="text/html", text="content")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebRTC webcam demo")
    parser.add_argument(
        "--host", default="127.0.0.1", help="Host for HTTP server (default: 10.236.66.97)"
    )
    parser.add_argument(
        "--port", type=int, default=8081, help="Port for HTTP server (default: 8080)"
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    fernet_key = fernet.Fernet.generate_key()
    f = fernet.Fernet(fernet_key)

    imgPresentations = []
    imgPresentations_ = getAllFaces()
    for i in range(len(imgPresentations_)):
        imgPresentations.append([float(i) for i in getAllFaces()[i][0][1:-1].split(',')])
    imgPresentations = np.array(imgPresentations)

    identity = []
    identity_ = getAllIden()
    for i in range(len(identity_)):
        identity.append(identity_[i][0])
    distances = np.sqrt(np.sum(np.multiply(imgPresentations, imgPresentations)))
    # print(run_onnx_extract_faces()[0].shape)
    # plt.imshow(run_onnx_extract_faces()[0])
    # print(run_onnx_presentation(run_onnx_extract_faces()[0]))
    # np.dot(小,大) / np.sqrt(np.sum(np.multiply(npT, npT))) * distanceB)
    app = web.Application()

    # 创建全局变量存储会议信息, 格式 会议号：[主讲人ID，主讲人配置,{ID：会议配置开启状态（默认可仅为接收）}]可以分析size，每个人进入的时候需要自带会议号
    app['meeting'] = {}
    # app['m'] = [1,2,3]
    # print(app['m'])
    # del app['m']
    # print(app['m'])

    setup(app, EncryptedCookieStorage(f))
    # 配置静态文件js css
    app.add_routes([web.static('/js', "./static/js")])
    app.add_routes([web.static('/css', "./static/css")])
    app.add_routes([web.static('/fonts', "./static/fonts")])
    app.add_routes([web.static('/images', "./static/images")])
    app.add_routes([web.static('/layui', "./static/layui")])

    # 配置template
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader('template'))

    env = aiohttp_jinja2.get_env(app)
    env.globals.update(zip=zip)

    app.on_shutdown.append(on_shutdown)
    app.router.add_post("/deal", deal)


    app.router.add_get("/", index)
    app.router.add_get("/register", register)
    app.router.add_get("/person/home", personHome)
    app.router.add_get("/person/check", personCheck)
    app.router.add_get("/person/apply", personApply)
    app.router.add_get("/person/info", personInfo)
    app.router.add_get("/person/meet", meet)
    app.router.add_get("/person/input", personInput)
    app.router.add_get("/person/sign", personSign)
    app.router.add_get("/person/overview", personOverview)

    app.router.add_get("/admin/home", adminHome)
    app.router.add_get("/admin/oa", adminOA)
    app.router.add_get("/admin/manage", adminManage)
    app.router.add_get("/admin/check", adminCheck)
    app.router.add_get("/admin/tableshow", tableShowAdmin)
    app.router.add_get("/admin/tableshowt", tableShow2Admin)
    app.router.add_get("/admin/meet", meet2)
    app.router.add_get("/admin/sign", adminsign)
    app.router.add_get("/admin/info", adminInfo)
    app.router.add_get("/admin/input", admininput)

    app.router.add_get("/receive", receive)
    app.router.add_get("/test", test)
    app.router.add_post("/offer", offer)
    web.run_app(app, host=args.host, port=args.port)
