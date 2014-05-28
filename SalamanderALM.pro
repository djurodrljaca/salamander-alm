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
    Database/BlobField.cpp \
    Database/BooleanField.cpp \
    Database/DateTimeField.cpp \
    Database/IntegerField.cpp \
    Database/NodeRecord.cpp \
    Database/NodeType.cpp \
    Database/SqliteDatabase.cpp \
    Database/TextField.cpp \
    View/ViewModel.cpp

SOURCES += \
    DataModel/DataModel.cpp \
    DataModel/Node.cpp

SOURCES += \
    main.cpp\
    MainWindow.cpp

HEADERS  += \
    Database/BlobField.h \
    Database/BooleanField.h \
    Database/DateTimeField.h \
    Database/IntegerField.h \
    Database/NodeRecord.h \
    Database/NodeType.h \
    Database/SqliteDatabase.h \
    Database/TextField.h \
    View/ViewModel.h

HEADERS  += \
    DataModel/DataModel.h \
    DataModel/Node.h

HEADERS  += \
    MainWindow.h

FORMS    += \
    MainWindow.ui

RESOURCES += \
    Resources/Database/Database.qrc
