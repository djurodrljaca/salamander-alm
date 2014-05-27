#-------------------------------------------------
#
# Project created by QtCreator 2014-05-24T15:02:06
#
#-------------------------------------------------

QT       += core gui sql

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = SalamanderALM
TEMPLATE = app

SOURCES += \
    main.cpp\
    MainWindow.cpp

SOURCES += \
    Database/Blob.cpp \
    Database/Boolean.cpp \
    Database/DateTime.cpp \
    Database/Integer.cpp \
    Database/Node.cpp \
    Database/NodeType.cpp \
    Database/SqliteDatabase.cpp \
    Database/Text.cpp

HEADERS  += \
    MainWindow.h

HEADERS  += \
    Database/SqliteDatabase.h \
    Database/Blob.h \
    Database/Boolean.h \
    Database/DateTime.h \
    Database/Integer.h \
    Database/Text.h \
    Database/Node.h \
    Database/NodeType.h

FORMS    += \
    MainWindow.ui

RESOURCES += \
    Resources/Database/Database.qrc
