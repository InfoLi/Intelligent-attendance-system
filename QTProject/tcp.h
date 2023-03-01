#ifndef TCP
#define TCP

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc_c.h>
#include <sys/socket.h>
#include <iostream>
#include <stdio.h>
#include <string>

#include <time.h>
#include <stdlib.h>
#include <algorithm>

#include <vector>

using namespace std;


#define __TCP_ECHO_TYPE_CLIENT 1 /* 客户端模式 */
#define __TCP_ECHO_TYPE_SERVER 2 /* 服务器模式 */
 /* 当前模式选择 */
#define __TCP_ECHO_TYPE (__TCP_ECHO_TYPE_CLIENT)
 /* 客户端 IP 地址 */
#define __TCP_ECHO_IP_CLIENT "192.168.232.1"
 /* 服务器 IP 地址 */
#define __TCP_ECHO_IP_SERVER "192.168.232.1"
#define __TCP_ECHO_PORT_CLIENT 8100 /* 客户端端口号 */
#define __TCP_ECHO_PORT_SERVER 8101 /* 服务器端口号 */
#define __TCP_ECHO_BUFF_SIZE_CLIENT 257 /* 客户端接收缓冲区大小 */
#define __TCP_ECHO_BUFF_SIZE_SERVER 257 /* 服务器接收缓冲区大小 */

static string split(vector<double> input){
    char* t;
    string st("");
    sprintf(t,"%.2lf",input[0]);
    st += string(t);
    for(int i=1;i<input.size();i++){
        sprintf(t,",%.2lf",input[i]);
        string temp(t);
        st += temp;
    }
    return st;
}

// string to vector<double>
static vector<double> split(string t) {
    int p1 = 0;
    int p2 = t.find(',');
    vector<double>* temp1 = new vector<double>();
    while (p2 != -1) {
        string temp = t.substr(p1, p2);
        temp1->push_back(strtod(temp.c_str(), 0));
        p1 = p2 + 1;
        t = t.substr(p1);
        p1 = 0;
        p2 = t.find(',');
    }
    temp1->push_back(strtod(t.c_str(), 0));
    return *temp1;
}


static cv::Mat __TcpEchoServer (void)
{
    int iRet = -1;
    int sockFd = -1;
    int sockFdNew = -1;
    /* 地址结构大小 */
    socklen_t uiAddrLen = sizeof(struct sockaddr_in);
    register ssize_t sstRecv = 0; /* 接收到的数据长度 */
    char cRecvBuff[__TCP_ECHO_BUFF_SIZE_SERVER] ={0};
    struct sockaddr_in sockaddrinLocal; /* 本地地址 */
    struct sockaddr_in sockaddrinRemote; /* 远端地址 */

    fprintf(stdout, "TCP echo server start.\n");
    sockFd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sockFd < 0) {
        fprintf(stderr, "TCP echo server socket error.\n");
        return cv::Mat();
    }
    /*
     * 初始化本地地址结构
     */
    memset(&sockaddrinLocal, 0, sizeof(sockaddrinLocal));
    sockaddrinLocal.sin_len = sizeof(struct sockaddr_in);
    /* 地址结构大小 */
    sockaddrinLocal.sin_family = AF_INET; /* 地址族 */
    sockaddrinLocal.sin_addr.s_addr = INADDR_ANY;
    /* 绑定服务器端口 */
    sockaddrinLocal.sin_port = htons(__TCP_ECHO_PORT_SERVER);
    iRet = bind(sockFd,(struct sockaddr *)&sockaddrinLocal,
            sizeof(sockaddrinLocal)); /* 绑定本地地址与端口 */
    if (iRet < 0) { /* 绑定操作失败 */
        close(sockFd); /* 关闭已经创建的 socket */
        fprintf(stderr, "TCP echo server bind error.\n");
        return cv::Mat(); /* 错误返回 */
    }
    listen(sockFd, 2);
    sockFdNew = accept(sockFd, (struct sockaddr *)&sockaddrinRemote, &uiAddrLen);
    if (sockFdNew < 0) {
        close(sockFd); /* 关闭已经创建的 socket */
        fprintf(stderr, "TCP echo server accept error.\n");
        return cv::Mat(); /* 错误返回 */
    }

    clock_t startTime = clock();
    clock_t endTime = clock();

    double maxTime = 1000*60*5;
    cv::Mat reMat;
    cv::Mat hctemp;//用於暫時存儲一行的圖片數據

    int height = 0;
    int width = 0;
    int point = 0;

    for (;;) {
        endTime = clock();
        if (endTime - startTime >= maxTime){
            break;
        }


        /* 清空接收缓冲区 */
        memset(&cRecvBuff[0], 0, __TCP_ECHO_BUFF_SIZE_SERVER);
        /* 从远端接收数据 */
        sstRecv = read(sockFdNew,
                (void *)&cRecvBuff[0],
                __TCP_ECHO_BUFF_SIZE_SERVER);
        if (sstRecv <= 0) { /* 接收数据失败 */
            if ((errno != ETIMEDOUT ) &&
                    (errno != EWOULDBLOCK)) { /* 非超时与非阻塞 */
                close(sockFdNew); /* 关闭已经连接的 socket */
                fprintf(stderr, "TCP echo server recvfrom error.\n");
                return cv::Mat(); /* 错误返回 */
            }
            continue; /* 超时或非阻塞后重新运行 */
        }

        //设置返回值
        const char* re = "complete\n";//必须要加上空白符
        sstRecv = strlen(re); /* 获取发送字符串长度 */

        //输出
        string result = &cRecvBuff[0];
        //sprintf(result,"%s\n",&cRecvBuff[0]);
        if(result[0] == 'h'){
            result = result.substr(2,result.size());
            char* te;
            height = strtol(result.c_str(),&te,10);
            write(sockFdNew, (const void *)re, sstRecv);
            continue;
        }else if(result[0] == 'w'){
            result = result.substr(2,result.size());
            char* te;
            width = strtol(result.c_str(),&te,10);
            write(sockFdNew, (const void *)re, sstRecv);
            continue;
        }

        vector<double> resultVector = split(result);
        cv::Mat tempMat(1,resultVector.size(),CV_8UC3,cv::Scalar(0,0,0));

        for(int i=0;i<resultVector.size();i++){
            tempMat.at<uchar>(0,i) = resultVector[i];
        }

        point += resultVector.size()/3;
        cv::hconcat(hctemp,tempMat,hctemp);
        if(point%width == 0 && point !=0){
            cv::vconcat(reMat,tempMat,reMat);
            tempMat = cv::Mat();
            point = 0;
        }



        //fprintf(stdout,"%.2lf",reslutVector[0]);
        //fprintf(stdout,"1");
        /* 将回射数据发回远端 */
        write(sockFdNew, (const void *)re, sstRecv);
    }
    close(sockFdNew);
    return reMat;
}


static int __TcpEchoClient (vector<string> n){
    int iRet = -1; /* 操作结果返回值 */
    int sockFd = -1; /* socket 描述符 */
    /* 地址结构大小 */
    socklen_t uiAddrLen = sizeof(struct sockaddr_in);
    register ssize_t sstRecv = 0; /* 接收到的数据长度 */
    register ssize_t sstSend = 0; /* 接收到的数据长度 */

    /* 接收缓冲区 */
    char cRecvBuff[__TCP_ECHO_BUFF_SIZE_CLIENT] ={0};
    struct sockaddr_in sockaddrinRemote; /* 远端地址 */

    fprintf(stdout, "TCP echo client start.\n");
    sockFd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sockFd < 0) {
        fprintf(stderr, "TCP echo client socket error.\n");
        return (-1);
    }
    /*
     * 初始化远端地址结构
     */
    /* 清空地址信息 */
    memset(&sockaddrinRemote, 0, sizeof(sockaddrinRemote));
    /* 地址转换错误 */
    if (!inet_aton(__TCP_ECHO_IP_SERVER, &sockaddrinRemote.sin_addr)) {
        close(sockFd); /* 关闭已经创建的 socket */
        fprintf(stderr, "TCP echo client get addr error.\n");
        return (-1); /* 错误返回 */
    }
    /* 地址结构大小 */
    sockaddrinRemote.sin_len = sizeof(struct sockaddr_in);
    sockaddrinRemote.sin_family = AF_INET; /* 地址族 */
    /* 绑定服务器端口 */
    sockaddrinRemote.sin_port = htons(__TCP_ECHO_PORT_SERVER);
    iRet = connect(sockFd,(const struct sockaddr *)&sockaddrinRemote,uiAddrLen);
    if (iRet < 0) { /* 操作失败 */
        fprintf(stderr, "TCP echo client connect error.\n");
        return (-1); /* 错误返回 */
    }

    //进行字符串的处理开始

    /* 需要发送的字符串 */
    //const char *pcSendData = "SylixOS Hello!\n";

    //开始发送数据
    for (int i =0;i<int(n.size());i++) {
        fprintf(stdout,"%d\n",i);
        const char *pcSendData = n[i].c_str();
        fprintf(stdout, "Send Data: %s\n", pcSendData);
        sstRecv = strlen(pcSendData); /* 获取发送字符串长度 */
        sstSend = write(sockFd,
                (const void *)pcSendData,sstRecv); /* 发送数据到指定的服务器端 */
        if (sstSend <= 0) { /* 发送数据失败 */
            if ((errno != ETIMEDOUT ) &&(errno != EWOULDBLOCK)) { /* 非超时与非阻塞 */
                close(sockFd); /* 关闭已经创建的 socket */
                fprintf(stderr, "TCP echo client write error.\n");
                return (-1); /* 错误返回 */
            }
            continue; /* 超时或非阻塞后重新运行 */
        }
        /* 清空接收缓冲区 */
        memset(&cRecvBuff[0], 0, __TCP_ECHO_BUFF_SIZE_CLIENT);

        /* 从远端接收数据 */
        sstRecv = read(sockFd,
                (void *)&cRecvBuff[0],
                __TCP_ECHO_BUFF_SIZE_SERVER);
        if (sstRecv <= 0) { /* 接收数据失败 */
            if ((errno != ETIMEDOUT ) &&
                    (errno != EWOULDBLOCK)) { /* 非超时与非阻塞 */
                close(sockFd); /* 关闭已经创建的 socket */
                fprintf(stderr, "TCP echo client read error.\n");
                return (-1); /* 错误返回 */
            }
            continue; /* 超时或非阻塞后重新运行 */
        }
        fprintf(stdout, "Recv Data: ");
        cRecvBuff[sstRecv] = 0;
        char status[8];
        sprintf(status,"%s",&cRecvBuff[0]);

        /////////////////////////////
        //将返回进行sqlite3的数据存储
        /////////////////////////////

        fprintf(stdout, "%s\n", status);
        sleep(5); /* 休眠一段时间 */
    }
    close(sockFd);
    return (0);
}


int startSignin(string account){
    string txt = "signin "+account;

    vector<string> input;
    input.push_back(txt);
    __TcpEchoClient(input);
}

cv::Mat startGetMat()
{
    cv::Mat result = __TcpEchoServer();

    return result;
}


#endif // TCP

