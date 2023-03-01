/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 4.8.7
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QHeaderView>
#include <QtGui/QLabel>
#include <QtGui/QMainWindow>
#include <QtGui/QMenuBar>
#include <QtGui/QPushButton>
#include <QtGui/QStatusBar>
#include <QtGui/QToolBar>
#include <QtGui/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QLabel *imgShowLabel;
    QPushButton *testNcnn;
    QPushButton *faceRegister;
    QPushButton *faceDetection;
    QPushButton *faceConfirm;
    QPushButton *keyPoint;
    QPushButton *drvier;
    QPushButton *open;
    QPushButton *faceRegister_3;
    QLabel *textLabel;
    QLabel *faceLabel;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(640, 480);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        imgShowLabel = new QLabel(centralWidget);
        imgShowLabel->setObjectName(QString::fromUtf8("imgShowLabel"));
        imgShowLabel->setGeometry(QRect(10, 50, 360, 360));
        testNcnn = new QPushButton(centralWidget);
        testNcnn->setObjectName(QString::fromUtf8("testNcnn"));
        testNcnn->setGeometry(QRect(10, 0, 91, 21));
        faceRegister = new QPushButton(centralWidget);
        faceRegister->setObjectName(QString::fromUtf8("faceRegister"));
        faceRegister->setGeometry(QRect(190, 0, 91, 21));
        faceDetection = new QPushButton(centralWidget);
        faceDetection->setObjectName(QString::fromUtf8("faceDetection"));
        faceDetection->setGeometry(QRect(10, 20, 91, 21));
        faceConfirm = new QPushButton(centralWidget);
        faceConfirm->setObjectName(QString::fromUtf8("faceConfirm"));
        faceConfirm->setGeometry(QRect(100, 0, 91, 21));
        keyPoint = new QPushButton(centralWidget);
        keyPoint->setObjectName(QString::fromUtf8("keyPoint"));
        keyPoint->setGeometry(QRect(190, 20, 91, 21));
        drvier = new QPushButton(centralWidget);
        drvier->setObjectName(QString::fromUtf8("drvier"));
        drvier->setGeometry(QRect(100, 20, 91, 21));
        open = new QPushButton(centralWidget);
        open->setObjectName(QString::fromUtf8("open"));
        open->setGeometry(QRect(280, 0, 41, 21));
        faceRegister_3 = new QPushButton(centralWidget);
        faceRegister_3->setObjectName(QString::fromUtf8("faceRegister_3"));
        faceRegister_3->setGeometry(QRect(280, 20, 41, 21));
        textLabel = new QLabel(centralWidget);
        textLabel->setObjectName(QString::fromUtf8("textLabel"));
        textLabel->setGeometry(QRect(120, 320, 270, 90));
        faceLabel = new QLabel(centralWidget);
        faceLabel->setObjectName(QString::fromUtf8("faceLabel"));
        faceLabel->setGeometry(QRect(20, 320, 90, 90));
        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 640, 26));
        MainWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QString::fromUtf8("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        MainWindow->setStatusBar(statusBar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MainWindow", 0, QApplication::UnicodeUTF8));
        imgShowLabel->setText(QApplication::translate("MainWindow", "<html><head/><body><p><br/></p></body></html>", 0, QApplication::UnicodeUTF8));
        testNcnn->setText(QApplication::translate("MainWindow", "testNcnn", 0, QApplication::UnicodeUTF8));
        faceRegister->setText(QApplication::translate("MainWindow", "faceRegister", 0, QApplication::UnicodeUTF8));
        faceDetection->setText(QApplication::translate("MainWindow", "faceDetction", 0, QApplication::UnicodeUTF8));
        faceConfirm->setText(QApplication::translate("MainWindow", "faceComfirm", 0, QApplication::UnicodeUTF8));
        keyPoint->setText(QApplication::translate("MainWindow", "keyPoint", 0, QApplication::UnicodeUTF8));
        drvier->setText(QApplication::translate("MainWindow", "driver", 0, QApplication::UnicodeUTF8));
        open->setText(QApplication::translate("MainWindow", "open", 0, QApplication::UnicodeUTF8));
        faceRegister_3->setText(QApplication::translate("MainWindow", "close", 0, QApplication::UnicodeUTF8));
        textLabel->setText(QString());
        faceLabel->setText(QString());
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
