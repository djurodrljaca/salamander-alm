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
    Database/SqliteDatabase.cpp \
    Database/DataTypes/Integer.cpp \
    Database/Tables/Node.cpp \
    Database/Tables/NodeType.cpp \
    Database/DataTypes/Text.cpp \
    Database/DataTypes/Boolean.cpp \
    Database/Tables/NodeAttributes.cpp \
    Database/DataTypes/DateTime.cpp \
    Database/Tables/Revision.cpp \
    Database/Tables/UserGroup.cpp \
    Database/Tables/UserGroupType.cpp \
    Database/Tables/User.cpp

HEADERS  += \
    MainWindow.h \
    Database/SqliteDatabase.h \
    Database/DataTypes/Integer.h \
    Database/Tables/Node.h \
    Database/Tables/NodeType.h \
    Database/DataTypes/Text.h \
    Database/DataTypes/Boolean.h \
    Database/Tables/NodeAttributes.h \
    Database/DataTypes/DateTime.h \
    Database/Tables/Revision.h \
    Database/Tables/UserGroup.h \
    Database/Tables/UserGroupType.h \
    Database/Tables/User.h

FORMS    += \
    MainWindow.ui

RESOURCES += \
    Resources/Database/Database.qrc
