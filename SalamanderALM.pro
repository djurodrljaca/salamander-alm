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
    MainWindow.cpp \
    DataModel/Node.cpp \
    Database/BlobField.cpp \
    Database/BooleanField.cpp \
    Database/DateTimeField.cpp \
    Database/IntegerField.cpp \
    Database/TextField.cpp \
    Database/NodeRecord.cpp

SOURCES += \
    Database/NodeType.cpp \
    Database/SqliteDatabase.cpp

SOURCES += \
    DataModel/DataModel.cpp

HEADERS  += \
    MainWindow.h \
    DataModel/NodeRecord.h \
    Database/BlobField.h \
    Database/BooleanField.h \
    Database/DateTimeField.h \
    Database/IntegerField.h \
    Database/TextField.h \
    Database/NodeRecord.h

HEADERS  += \
    Database/SqliteDatabase.h \
    Database/NodeType.h

HEADERS  += \
    DataModel/DataModel.h

FORMS    += \
    MainWindow.ui

RESOURCES += \
    Resources/Database/Database.qrc
