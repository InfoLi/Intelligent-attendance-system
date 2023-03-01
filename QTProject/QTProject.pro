#-------------------------------------------------
#
# Project created by QtCreator 2022-06-16T22:22:07
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = QTProject
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp

HEADERS  += mainwindow.h \
    testfornet.h \
    mtcnn.h \
    mtc.h \
    sqlite4project.h \
    facenet128.h \
    tcp.h

FORMS    += mainwindow.ui

unix:!macx: LIBS += -L$$PWD/opencv/lib -lopencv_videoio -latomic
unix:!macx: LIBS += -L$$PWD/x86/ -lncnn -latomic
unix:!macx: LIBS += -L$$PWD/sqlite3/ -lsqlite3 -latomic

INCLUDEPATH += $$PWD/opencv/include
DEPENDPATH += $$PWD/opencv/lib
INCLUDEPATH += $$PWD/ncnnNet/
DEPENDPATH += $$PWD/x86/
INCLUDEPATH += $$PWD/sqlite3/
DEPENDPATH += $$PWD/sqlite3/
