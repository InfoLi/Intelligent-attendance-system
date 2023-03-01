#ifndef SQLITE4PROJECT
#define SQLITE4PROJECT

#include <sqlite3.h>
#include <iostream>
#include <stdio.h>
#include <vector>
#include <stdlib.h>
#include <algorithm>
#include <QDataStream>

#include <opencv2/opencv.hpp>

using namespace std;

namespace sql{
    class QTSql{
    private:
        sqlite3 * sql;//sql连接用
        string dbName;
        string cmd;//指令存储
        char *zErrMsg = 0;//sql用？
        bool executeSuccess;//是否执行成功，事务用
        vector<string> returnDate;
    public:
        QTSql(){
            dbName = "test.db";
            cmd = "";
        };
        QTSql(string db){
            dbName = db;
            cmd = "";
        };
        ~QTSql(){
            sqlite3_free(zErrMsg);
        }

        //double[] to string
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

        /*
        static double** transform(vector<vector<double> >* tv){
            double ** re = new double[];
            for (int i = 0; i < (int)tv->size(); i++) {
                    for (int j = 0; j < (*tv)[i].size(); j++) {
                        cout << (*tv)[i][j] << endl;
                }
            }
        }
        */

        static void show(vector<string >* tv){
            for (int i = 0; i < (int)tv->size(); i++) {
                    cout << (*tv)[i] << endl;
                }
        }

        static int callback(void *NotUsed, int argc, char **argv, char **azColName){
           int i;
           for(i=0; i<argc; i++){
              printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
           }
           printf("\n");
           return 0;
        }

        //select的回调函数
        static int callbackSelect(void *data, int argc, char **argv, char **azColName){
           int i;
           for(i=0; i<argc; i++){
              printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
           }
           //delete data;
           //data = new string("YES!");//测试完成，可以把值传回来
           printf("\n");
           return 0;
        }

        //这将是含有JSON格式的存储处理//项目专用
        static int callbackJSON(vector<string > *data, int argc, char **argv, char **azColName){
            string t = string(argv[0]);
            try{
                data->push_back(t);
            }catch(exception e){
                cout << e.what() << endl;
            }

            return 0;
        }

        //测试数据库文件是否存在，不存在便直接
        void testDB(){
            int re = sqlite3_open("./test.db",&sql);
            if(re == 0){
                cout << "Open sqlite successful" << endl;
            }else{
                cout << "Open sqlite failed" << endl;
            }
        }

        //创建表//complete
        void sqlCreateTable(){
            //事务开始
            sqlite3_exec(sql,"begin",0,0,&zErrMsg);

            string table = "create table if not exists userInfo(userId integer not null primary key autoincrement,userName varchar(20))";

            int rc = sqlite3_exec(sql,table.c_str(),callback,0,&zErrMsg);

            if(rc == SQLITE_OK){
                executeSuccess = true;
                sqlite3_free(zErrMsg);
            }else{
                cout << "ERROR:" << zErrMsg << endl;
                executeSuccess = false;
                sqlite3_free(zErrMsg);
            }


            //事务结束
            if(executeSuccess == true){
                sqlite3_exec(sql,"commit",0,0,0);
            }else{
                sqlite3_exec(sql,"callback",0,0,0);
            }
        }

        //创建用户Mat表
        void sqlCreateMat(){
            //事务开始
            sqlite3_exec(sql,"begin",0,0,&zErrMsg);

            string table = "create table if not exists userMat(count integer,userMat byte)";

            int rc = sqlite3_exec(sql,table.c_str(),callback,0,&zErrMsg);

            if(rc == SQLITE_OK){
                executeSuccess = true;
                sqlite3_free(zErrMsg);
            }else{
                cout << "ERROR:" << zErrMsg << endl;
                executeSuccess = false;
                sqlite3_free(zErrMsg);
            }


            //事务结束
            if(executeSuccess == true){
                sqlite3_exec(sql,"commit",0,0,0);
            }else{
                sqlite3_exec(sql,"callback",0,0,0);
            }
        }

        /*
        //插入人脸识别信息
        void sqlInserInfo(string name,double data[128]){
            //事务开始
            sqlite3_exec(sql,"begin",0,0,&zErrMsg);

            string cmd = "insert into userInfo values("+name+",json_object('data':";

            //使用sprintf进行格式转换
            sprintf()

            for(int i=1;i<128;i++){
                cmd += ","+std::to_string(data[i]);
            }

            cmd += "));";

            int rc = sqlite3_exec(sql,cmd.c_str(),callback,0,&zErrMsg);

            if(rc == SQLITE_OK){
                executeSuccess = true;
                sqlite3_free(zErrMsg);
            }else{
                cout << "ERROR:" << zErrMsg << endl;
                executeSuccess = false;
                sqlite3_free(zErrMsg);
            }

            //事务结束
            if(executeSuccess == true){
                sqlite3_exec(sql,"commit",0,0,0);
            }else{
                sqlite3_exec(sql,"callback",0,0,0);
            }
        }
        */

        //获取人脸信息
        string sqlSelect(string name){
            //事务开始
            sqlite3_exec(sql,"begin",0,0,&zErrMsg);
            sqlite3_stmt *stmt = NULL;

            string cmd = "select userName from userInfo where userId = '"+name+"';";

            string data;

            int rc = sqlite3_prepare_v2(sql,cmd.c_str(),-1,&stmt,NULL);

            if(rc == SQLITE_OK){
                while (sqlite3_step(stmt) == SQLITE_ROW) {
                    // 取出第0列字段的值
                    data = string(sqlite3_column_text(stmt, 0));
                }
                executeSuccess = true;
                sqlite3_free(zErrMsg);
            }else{
                cout << "ERROR:" << zErrMsg << endl;
                executeSuccess = false;
                sqlite3_free(zErrMsg);
            }
//            cout << "Start commit" << endl;

            //事务结束
            if(executeSuccess == true){
//                cout << "COMMIT" << endl;
                sqlite3_exec(sql,"commit",0,0,0);
//            }else{
//                cout << "ERROR" << endl;
                sqlite3_exec(sql,"callback",0,0,0);
            }

            return data;
        }

        //执行sql命令
        void sqlExecute(string cmd,bool select = false){
            //事务开始
            sqlite3_exec(sql,"begin",0,0,&zErrMsg);
            int rc = 0;

            string *data = new string("YES?");//值传递测试

            if(select == false)
                rc = sqlite3_exec(sql,cmd.c_str(),callback,0,&zErrMsg);
            else
                rc = sqlite3_exec(sql,cmd.c_str(),callbackSelect,data,&zErrMsg);

            //cout << *data << endl;
            if(rc == SQLITE_OK){
                executeSuccess = true;
                sqlite3_free(zErrMsg);
            }else{
                cout << "ERROR:" << zErrMsg << endl;
                executeSuccess = false;
                sqlite3_free(zErrMsg);
            }

            //事务结束
            if(executeSuccess == true){
                sqlite3_exec(sql,"commit",0,0,0);
            }else{
                sqlite3_exec(sql,"callback",0,0,0);
            }
        }

        //将mat文件存入数据库
        void sqlInsertMat(cv::Mat &sift){

        }
    };

    ////////////////////////////////////
    /// Mat计算整体的余弦相似度
    ///////////////////////////////////
    // 输入所有的用户组成的矩阵，用于识别的矩阵，用户集的第几行，返回余弦相似度
    // input：[1,n] [1,n] n =128
    static double  cosine_similariy(cv::Mat t1,cv::Mat t2){
        double r = 0;
        double r1 = 0;
        double r2 = 0;

        int w = t1.cols;

        for (int i = 0; i < w; i++) {
            r += t1.at<double>(0, i) * t2.at<double>(0,i);
            r1 += pow(t1.at<double>(0, i), 2);
            r2 += pow(t2.at<double>(0, i), 2);
        }

        r1 = sqrt(r1);
        r2 = sqrt(r2);

        if(r1 == 0 || r2 == 0){
            return 0;
        }

        return r/(r1*r2);
    }

    // 输入全部员工的人脸识别数据[n,128], 刚刚识别的人脸数据[1, 128]
    static vector<double> faceComfirm(cv::Mat userInfo,cv::Mat input){
        if(input.empty()){
            return vector<double>();
        }
        vector<double> result;

        //计算余弦相似度
        for(int i =0;i<userInfo.rows;i++){
            double temp = cosine_similariy(userInfo.row(i),input);
            result.push_back(temp);
        }

        if(result.size() == 0){
            return vector<double>();
        }
        return result;

    }

    // 输入所有的用户组成的矩阵，用于识别的矩阵，用户集的第几行，返回余弦相似度
    // input：[1,n] [1,n] n =128
    // 重載函數
    static double  cosine_similariy(cv::Mat t1,vector<float> t2){
        double r = 0;
        double r1 = 0;
        double r2 = 0;

        int w = t1.cols;

        for (int i = 0; i < w; i++) {
            r += t1.at<double>(0, i) * t2[i];
            r1 += pow(t1.at<double>(0, i), 2);
            r2 += pow(t2[i], 2);
        }

        r1 = sqrt(r1);
        r2 = sqrt(r2);

        if(r1 == 0 || r2 == 0){
            return 0;
        }

        return r/(r1*r2);
    }

    // 输入全部员工的人脸识别数据[n,128], 刚刚识别的人脸数据[1, 128]
    //重載函數
    static vector<float> faceComfirm(cv::Mat userInfo,vector<float> input){
        if(input.empty()){
            return vector<float>();
        }
        vector<float> result;

        //计算余弦相似度
        for(int i =0;i<userInfo.rows;i++){
            float temp = cosine_similariy(userInfo.row(i),input);
            result.push_back(temp);
        }

        if(result.size() == 0){
            return vector<float>();
        }
        return result;

    }

    //获取最符合的员工
    static int getMyTarget(vector<double> input){
        if(input.size() == 0){
            return 0;
        }

        int index = max_element(input.begin(),input.end()) - input.begin();;
        cout << input[index] << endl;
        return index;
    }

    //获取最符合的员工
    //float版重載
    static int getMyTarget(vector<float> input){
        if(input.size() == 0){
            return 0;
        }

        int index = max_element(input.begin(),input.end()) - input.begin();;
        cout << input[index] << endl;
        return index;
    }

    ///////////////////////////////////////
    ///// XML操作
    ///////////////////////////////////////
    //写入
    static bool XMLWrite(cv::Mat input) {
        if (input.empty()) {
            return false;
        }
        //input.convertTo(input, CV_64FC1);
        cv::FileStorage fs("./data.xml", cv::FileStorage::WRITE);
        fs << "faceData" << input;
        fs.release();
        return true;
    }

    //读取
    static cv::Mat XMLRead() {
        cv::Mat re;
        cv::FileStorage fs("./data.xml", cv::FileStorage::READ);

        fs["faceData"] >> re;

        if (re.empty()) {
            return re;
        }

        fs.release();

        return re;
    }

    //改变
    static bool XMLChange(int targetRow, cv::Mat data) {
        if (data.empty()) {
            return false;
        }
        //data.convertTo(data, CV_64FC1);

        //读取
        cv::Mat re;
        cv::FileStorage fs("./data.xml", cv::FileStorage::READ);

        fs["faceData"] >> re;
        fs.release();

        //改变数据
        data.copyTo(re.row(targetRow));


        //写入
        cv::FileStorage fs1("./data.xml", cv::FileStorage::WRITE);
        fs1 << "faceData" << re;
        fs1.release();

        return true;
    }

    //增加
    static bool XMLAppend(cv::Mat& data, cv::Mat input) {
        if (data.empty()) {
            return false;
        }

        if (data.cols != input.cols) {
            return false;
        }

        data.push_back(input);
        cout << data.rows;

        cv::FileStorage fs1("./data.xml", cv::FileStorage::WRITE);
        fs1 << "faceData" << data;
        fs1.release();

        return true;
    }

    //增加
    static bool XMLAppend(cv::Mat& data) {
        if (data.empty()) {
            return false;
        }

        cv::Mat input = XMLRead();

        input.push_back(data);
        cout << data.rows;

        cv::FileStorage fs1("./data.xml", cv::FileStorage::WRITE);
        fs1 << "faceData" << input;
        fs1.release();

        return true;
    }

    //删除
    static bool XMLRemove(cv::Mat& data, int rowNum) {
        if (data.empty()) {
            return false;
        }

        if (data.rows < rowNum) {
            return false;
        }

        cv::Mat re;
        int target = rowNum - 1 >= 0?rowNum - 1:0;

        for (int i = 0; i < data.rows; i++) {
            if(i != target)
                re.push_back(data.row(i));
        }

        data = re.clone();

        cv::FileStorage fs1("./data.xml", cv::FileStorage::WRITE);
        fs1 << "faceData" << data;
        fs1.release();

        return true;
    }
}


#endif // SQLITE4PROJECT

