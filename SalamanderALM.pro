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
    Database/UserType.cpp \
    Database/UserRecord.cpp \
    Database/RevisionRecord.cpp \
    NewProjectDialog.cpp \
    Database/NodeNameRecord.cpp \
    Database/NodeDescriptionRecord.cpp \
    Database/NodeAttributesRecord.cpp

SOURCES += \
    DataModel/Node.cpp \
    DataModel/TreeViewModel.cpp

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
    Database/UserType.h \
    Database/UserRecord.h \
    Database/RevisionRecord.h \
    NewProjectDialog.h \
    Database/NodeNameRecord.h \
    Database/NodeDescriptionRecord.h \
    Database/NodeAttributesRecord.h

HEADERS  += \
    DataModel/Node.h \
    DataModel/TreeViewModel.h

HEADERS  += \
    MainWindow.h

FORMS    += \
    MainWindow.ui \
    NewProjectDialog.ui

RESOURCES += \
    Resources/Database/Database.qrc
