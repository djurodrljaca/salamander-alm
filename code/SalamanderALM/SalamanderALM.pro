#-------------------------------------------------
#
# Project created by QtCreator 2014-05-24T15:02:06
#
#-------------------------------------------------

QT       += core gui sql

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = SalamanderALM
TEMPLATE = app


SOURCES += main.cpp\
        MainWindow.cpp \
    SqliteDatabase.cpp \
    DatabaseId.cpp

HEADERS  += MainWindow.h \
    SqliteDatabase.h \
    DatabaseId.h

FORMS    += MainWindow.ui

RESOURCES += \
    Resources/Database/Database.qrc
