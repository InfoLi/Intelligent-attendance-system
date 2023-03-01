#ifndef MAINWINDOW_H
#define MAINWINDOW_H


#include <opencv2/opencv.hpp>
#include <opencv2/videoio/videoio.hpp>
#include <QPaintEvent>
#include <QTimer>
#include <QPainter>
#include <QPixmap>
#include <QLabel>
#include <QImage>
#include <QTimer>
#include <QMainWindow>
#include <iostream>
#include <QTime>
#include "sqlite4project.h"


namespace Ui {
enum func_set {ncnn,faceComfirm,faceRegister,faceDetection,driver,keyPoint};
class MainWindow;
}



class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
    void changeImg(cv::Mat img);//改变类的图片
    void readImg();//测试用：用于读取用于传输图片的文件
    void showImg();//用于展示传输用的图片
    void changeText(std::string input,std::string background="QLabel{background-color:rgb(200,101,102);}");//用于改变text标签
    void showFace(int temp);//用于展示人脸
    static QImage transImg(cv::Mat img);//用于进行图片转换的静态函数
    void getComfirmResult(vector<float> result);
    sql::QTSql sqlcon;
private slots:
    void updateImage();

    void on_faceRegister_clicked();

    void on_faceConfirm_clicked();

    void on_open_clicked();

    void on_faceRegister_3_clicked();

    void on_faceDetection_clicked();

    void on_testNcnn_clicked();

    void on_drvier_clicked();

    void on_keyPoint_clicked();

private:

    Ui::func_set funcSet;
    Ui::MainWindow *ui;
    QImage showImage;
    cv::VideoCapture capture;
    QTimer theTimer;
    QTime clickCamera;
    cv::Mat srcImage;
    cv::Mat image_fliped;
protected:
    void MainWindow::paintEvent(QPaintEvent *e);
};

#endif // MAINWINDOW_H

/*
//以下一个函数用于测试图片是否可以正常展示
void MainWindow::readImg(){
    cv::Mat img = cv::imread("./1.jpg");
    //进行格式转换
    cvtColor(img, img, CV_BGR2RGB);
    //进行opencv和Qt的图片模式转换
    QImage img2 = QImage((const unsigned char*)(img.data), img.cols, img.rows, img.step, QImage::Format_RGB888);
    ui->imgShowLabel->setPixmap(QPixmap::fromImage(img2));
    ui->imgShowLabel->resize(img2.size());//进行尺寸的改变
    ui->imgShowLabel->show();
}

//用于改变图片的尝试
void MainWindow::on_pushButton_2_clicked()
{
    //this->readImg();
    //this->showImg();
}
*/
