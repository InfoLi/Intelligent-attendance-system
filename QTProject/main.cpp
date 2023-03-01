#include "mainwindow.h"
#include <QApplication>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <vector>
#include <string>
#include <cstring>

using namespace cv;
using namespace std;

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    sql::QTSql s = sql::QTSql();
//    s.testDB();
//    s.sqlCreateTable();

////    s.sqlExecute("select * from userInfo",true);

//    char nu[3];
//    sprintf(nu,"%d",1);
//    try{
//        string re =s.sqlSelect(string(nu));
//        std::cout << re << endl;
//    }catch(Exception e){
//        std::cout <<e.what() << endl;
//    }

    return a.exec();
}

/*
    cv::Mat testImg(30, 128, CV_64FC1, Scalar(0.0, 0.0, 0.0));

    for (int i = 0; i < 30; i++) {
        for (int j = 0; j < 128; j++) {
            testImg.at<double>(i, j) = i * j / (30.0 * 128.0);
        }
    }

    sql::XMLWrite(testImg);

    cv::Mat black(1, 128, CV_64FC1, Scalar(0.0, 0.0, 0.0));
    sql::XMLChange(26,black);
    cv::Mat re = sql::XMLRead();

    cout << re << endl;
*/

//sql::QTSql s = sql::QTSql();
//s.testDB();
//s.sqlCreateTable();
//s.sqlCreateMat();
//s.sqlExecute("create table test(id int,name varchar(10));insert into test values(3,'tester')");
//s.sqlExecute("select * from test;",true);
//s.sqlExecute("drop table test;create table test(id int,data JSON);insert into test values(3,'{'id':'test','name':'wtf'}')");
//s.sqlExecute("insert into test values(3,'{\"id\":\"tester\"}')");

/*
double test[5]{1.1,4.5,0.14,0.2,3.5};
char* t;
string st("");
sprintf(t,"%.2lf",test[0]);
st += string(t);
for(int i=1;i<5;i++){
    sprintf(t,",%.2lf",test[i]);
    string temp(t);
    st += temp;
}

s.sqlExecute("delete from userInfo");
s.sqlExecute("insert into userInfo values (0,'test','"+st+"')");
s.sqlExecute("select * from userInfo",true);
*/

//s.sqlExecute("select * from userInfo",true);

/*
vector<vector<double> >* data = s.sqlSelect("test");
sql::QTSql::show(data);
s.sqlExecute("select * from userInfo",true);
*/
//s.sqlExecute("insert into userInfo values (0,'tester','[1,1,4.5,1.4]'')");
//vector<vector<double> >* data = s.sqlSelect("test");
//sql::QTSql::show(data);

/*
vector<double> test = vector<double>();
double tt[5]{1.1,2.3,3.4,4.5,5.6};
for(int i =0;i<5;i++){
    test.push_back(tt[i]);
}
string S = sql::QTSql::split(test);
cout << S << endl;
*/

//s.sqlExecute("drop table userMat;");
