#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "testfornet.h"
#include "mtc.h"
#include "facenet128.h"
#include "tcp.h"
#include "sqlite4project.h"

#include <QDateTime>
#include <QDebug>
#include <QFileDialog>


using namespace cv;
extern cv::Mat reImg;

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    sqlcon = sql::QTSql();
    sqlcon.testDB();
    sqlcon.sqlCreateTable();

    ui->setupUi(this);
    //用于刷新视频流用
    connect(&theTimer, SIGNAL(timeout()), this, SLOT(updateImage()));
}

MainWindow::~MainWindow(){
    delete ui;
}

void MainWindow::changeText(std::string input,std::string background="QLabel{background-color:rgb(200,101,102);}"){
    ui->textLabel->setText(QString::fromStdString(input));
    ui->textLabel->setStyleSheet(QString::fromStdString(background));//"QLabel{background-color:rgb(200,101,102);}"
}

//若图片开启后自动更新图片用的函数
void MainWindow::paintEvent(QPaintEvent *e)
{
    if(capture.isOpened()){//必须是摄像头已经开启，否则不会进行转换
        cv::resize(image_fliped,image_fliped,cv::Size(ui->imgShowLabel->height(),ui->imgShowLabel->width()));
        QImage image1 = QImage((uchar*)(image_fliped.data), image_fliped.cols, image_fliped.rows, QImage::Format_RGB888);
        ui->imgShowLabel->setPixmap(QPixmap::fromImage(image1));
        //ui->imgShowLabel->resize(image1.size());
        ui->imgShowLabel->show();
    }
}

void MainWindow::getComfirmResult(vector<float> result){
    cv::Mat allData = sql::XMLRead();
    vector<float> re = sql::faceComfirm(allData,result);
    int index =  sql::getMyTarget(re);
    if(re[index] >= 0.4){
        char indexc[12];
        sprintf(indexc,"%d",index);
        //获取最大值下标
        std::cout << index << std::endl;
        string result2 = sqlcon.sqlSelect(string(indexc));
        std::cout << result2 << endl;
        //签到
        startSignin("12314");
        changeText(result2);
        showFace(0);
    }
}

void MainWindow::updateImage()
{
    if(capture.isOpened()){
        capture>>srcImage;
        /// 将Image图片处理后进行返回返回，用于人脸识别
        /// Image = function()
        if(funcSet == Ui::faceComfirm){
            int sec = clickCamera.elapsed();
            //第三秒进行帧的人脸识别
            if(sec >= 6000){//用于每隔三秒就会进行一次识别
                clickCamera.start();
                // 识别函数
                // 函数要求cv::Mat function(cv::Mat srcImg)
                // srcImage = function()
                cv::Mat temp = faceDetectionAPI(srcImage);
                try{
                    if(!temp.empty()){
                        srcImage = temp;

                        //已经获取了截取的图片了
                        //imwrite("temp.jpg",temp);
                        cv::Mat tt = imread("imsave.jpg");
                        showFace(1);

                        //人脸识别进行
                        vector<float> result = facenet128::facenet(tt);

                        ///////////////////////////////////////////
                        //////////  余弦相似度需要进行检测
                        /// ///////////////////////////////////////

                        //計算餘弦相似度
                        // 如果不满足则会不会显示
                        getComfirmResult(result);
                    }
                }catch(Exception e){
                    std::cout << e.what() << endl;
                }
            }
            //第1秒后将显示人脸的标签还原为透明
            if(sec >= 1000 && sec <= 1250){
                changeText("","QLabel {background-color: transparent;}");
                showFace(1);
                //showFace(cv::Mat(1,1,CV_8SC3,cv::Scalar(0,0,0)));
            }
        }


        //将会用于其他函数进行实现
        if(funcSet == Ui::ncnn){

        }

        //srcImage = testNcnn::getResult(srcImage);
        cv::flip(srcImage, image_fliped, 1);
        if(image_fliped.data)
        {
            cvtColor(image_fliped, image_fliped, CV_BGR2RGB);//Qt中支持的是RGB图像, OpenCV中支持的是BGR
            this->update();  //发送刷新消息
        }else{
            std::cout << "Capture Error: can't get image from camera" << std::endl;
        }

    }
}

//人脸识别用：进行人脸效果展示
//还需要把图片设置为透明
void MainWindow::showFace(int temp=0){
    if(temp == 0){
        cv::Mat faceImage = imread("imsave.jpg");
        QPixmap mmp = QPixmap::fromImage(transImg(faceImage));
        mmp = mmp.scaled(ui->faceLabel->size());
        ui->faceLabel->setPixmap(mmp);
        ui->faceLabel->resize(mmp.size());
        ui->faceLabel->show();
    }else{
        ui->faceLabel->setText(" ");
    }
}

//用于转换图片后更换展示用图片
void MainWindow::changeImg(Mat img){
    showImage = MainWindow::transImg(img);
}

//用于转换图片
QImage MainWindow::transImg(Mat img){
    cvtColor(img, img, CV_BGR2RGB);
    //进行opencv和Qt的图片模式转换
    QImage img2 = QImage((const unsigned char*)(img.data), img.cols, img.rows, img.step, QImage::Format_RGB888);
    return img2;
}

//用于展示图片
void MainWindow::showImg(){
    //展示图片
    showImage = showImage.scaled(QSize(ui->imgShowLabel->width(),ui->imgShowLabel->height()));
    std::cout << showImage.width() << "x" << showImage.height() << std::endl;
    ui->imgShowLabel->setPixmap(QPixmap::fromImage(showImage));
    //ui->imgShowLabel->resize(showImage.size());
    ui->imgShowLabel->show();
}

//用于测试ncnn模型
void MainWindow::on_testNcnn_clicked()
{
    funcSet =Ui::ncnn;
    MainWindow::changeImg(testNcnn::getTrainResult());
}

//人脸注册（拍照）
void MainWindow::on_faceRegister_clicked(){
    funcSet =Ui::faceRegister;
    char image_name[64] = "face.jpg";
    cv::Mat frame1;

    if(!capture.isOpened()){
        this->on_open_clicked();
    }
    capture >> frame1;

    //保存图片
    if (frame1.empty())
    {
        std::cout << "frame1 is empty" << std::endl;
    }else{
        std::cout<< "frame1.size= "<<frame1.size<<std::endl;

        std::cout<<image_name<<std::endl;
        //保存图片
        cv::imwrite(image_name, frame1);

        //////////////////////////////////////////////////////
        /// 此处为生产128维人脸识别数据，并存入数据库
        //////////////////////////////////////////////////////
        //獲取維度
        vector<float> result = facenet128::facenet(frame1);
        cv::Mat data = cv::Mat(1,128,CV_64FC1,cv::Scalar(0,0,0));
        for(int i=0;i<128;i++){
            data.at<float>(0,i) = result[i];
        }

        //將數據插入XML文件
        sql::XMLAppend(data);

        //將姓名等插入數據庫
        sqlcon.sqlExecute("insert into userInfo select count(userId),'Yinlianlei' from userInfo;");

        cout << "注冊成功" << endl;
    }
    //显示图片
    QPixmap mmp = QPixmap::fromImage(transImg(frame1));
    mmp = mmp.scaled(ui->imgShowLabel->size());
    ui->imgShowLabel->setPixmap(mmp);
}

//视频流用再次点击进行
//人脸识别（视频流）
void MainWindow::on_faceConfirm_clicked(){
    funcSet =Ui::faceComfirm;
    if(capture.isOpened()){
        capture.release();
    }
    if (capture.open(200)) {
        std::cout<<"Camera open succeed."<<std::endl;
        //从摄像头捕获视频
        srcImage = Mat::zeros(capture.get(CV_CAP_PROP_FRAME_HEIGHT), capture.get(CV_CAP_PROP_FRAME_WIDTH), CV_8UC3);
        theTimer.start(33);
    }else {
        std::cout<<"Camera open failed"<<std::endl;
        capture.release();
    }
    //打开视频流
}



//人脸检测(选择本地文件)( )
void MainWindow::on_faceDetection_clicked(){
    funcSet =Ui::faceDetection;
    //参数，选择ui框体，窗口名称，默认路径，过滤类型
    QString selectImg = QFileDialog::getOpenFileName(this,"select image","./","images(*.png *.jpg *jpeg *bmp);;");
    if(selectImg.isEmpty()){
        std::cout << "EMPTY IMAGE" << std::endl;
    }else{
        cv::Mat tempImg = cv::imread(selectImg.toStdString());
        if(tempImg.empty()){
            std::cout << "EMPTY IMG" << std::endl;
        }

        //进行人脸检测
        tempImg = faceDetectionAPI(tempImg);

        //人脸识别
        try{
            vector<float> result = facenet128::facenet(tempImg);

            for(int i=0;i<128;i++){
                cout << result[i] << "\t";
            }
            cout << endl;

        }catch(Exception e){
            cout << e.what() << endl;
        }

        //tempImg = testNcnn::getResult(tempImg);
        cvtColor(tempImg, tempImg, COLOR_BGR2RGB);

        //进行图片的转换
        showImage = this->transImg(tempImg);
        //this->changeImg(tempImg);
        this->changeText("comfirm");
        this->showImg();
    }
}

//疲劳驾驶
void MainWindow::on_drvier_clicked(){
    funcSet =Ui::driver;
    if(capture.isOpened()){
        capture.release();
    }
    if (capture.open(200)) {
        std::cout<<"Camera open succeed."<<std::endl;
        //从摄像头捕获视频
        srcImage = Mat::zeros(capture.get(CV_CAP_PROP_FRAME_HEIGHT), capture.get(CV_CAP_PROP_FRAME_WIDTH), CV_8UC3);

        ////////////////////////////////////////////////
        /// 将srcImage图片处理后进行返回返回，用于疲劳驾驶
        /// srcImage = function()
        ////////////////////////////////////////////////

        theTimer.start(33);
    }else {
        std::cout<<"Camera open failed"<<std::endl;
        capture.release();
    }
    //打开视频流
}

//特征点标记
//由是否开启摄像头来决定采用的方式
void MainWindow::on_keyPoint_clicked(){
    funcSet =Ui::keyPoint;
    if(capture.isOpened()){
        std::cout<<"Camera open succeed."<<std::endl;
        //从摄像头捕获视频
        srcImage = Mat::zeros(capture.get(CV_CAP_PROP_FRAME_HEIGHT), capture.get(CV_CAP_PROP_FRAME_WIDTH), CV_8UC3);

        ////////////////////////////////////////////////
        /// 将srcImage图片处理后进行返回返回，用于摄像头识别
        /// srcImage = function()
        ////////////////////////////////////////////////

        theTimer.start(33);
    }else{
        //参数，选择ui框体，窗口名称，默认路径，过滤类型
        QString selectImg = QFileDialog::getOpenFileName(this,"select image","./","images(*.png *.jpg *jpeg *bmp);;");
        if(selectImg.isEmpty()){
            std::cout << "EMPTY IMAGE" << std::endl;
        }else{
            cv::Mat tempImg = cv::imread(selectImg.toStdString());
            if(tempImg.empty()){
                std::cout << "EMPTY IMG" << std::endl;
            }
            //cvtColor(tempImg, tempImg, COLOR_BGR2RGB);


            //////////////////////////////////////////////////////////////////
            /// 这里用于将图片进行标记，返回值必须为Mat或QImage的其中一种
            //////////////////////////////////////////////////////////////////


            this->changeImg(tempImg);
            this->showImg();
        }
    }
}

//以下两个功能基本上用于拍摄
//开启摄像头(√)
void MainWindow::on_open_clicked(){
    //funcSet =Ui::ncnn;
    //std::cout << funcSet << std::endl;
    if (capture.isOpened()){
        std::cout << "camera is opening" << std::endl;
        return;
    }else{
        if (capture.open(200)) {
            std::cout<<"camera opened"<<std::endl;
            //从摄像头捕获视频
            srcImage = Mat::zeros(capture.get(CV_CAP_PROP_FRAME_HEIGHT), capture.get(CV_CAP_PROP_FRAME_WIDTH), CV_8UC3);
            theTimer.start(33);//更新视频流用，0.1秒刷新一次
            clickCamera.start();
        }else{
            std::cout << "open camera failed" << std::endl;
        }
        //打开视频流
    }
}

//关闭摄像头(√)
void MainWindow::on_faceRegister_3_clicked(){
    if(capture.isOpened()){
        std::cout << "camera down" << std::endl;
        capture.release();
    }
}

//sql::QTSql s = sql::QTSql();
//s.testDB();
//s.sqlExecute("drop table userInfo;");
//s.sqlCreateTable();

//插入员工数据，id为员工在Mat上的数据，userName为员工姓名
//s.sqlExecute("insert into userInfo select count(userId),'Yinlianlei3' from userInfo;");
//s.sqlExecute("select * from userInfo",true);

/*
cv::Mat img = sql::XMLRead();//读取数据
cv::Mat imgInput(1, 128, CV_64FC1, Scalar(0.0, 0.0, 0.0));

for (int j = 0; j < 128; j++) {
    imgInput.at<double>(0, j) = pow(j/128.0,2);
}

//进行人脸检测
vector<double> re = sql::faceComfirm(img,imgInput);
for(int i =0;i<30;i++){
    cout << re[i] << "\t";
}
cout << endl;

//获取最大值下标
cout << sql::getMyTarget(re) << endl;

//删除
cv::Mat re = sql::XMLRead();

sql::XMLRemove(re,0);
*/


