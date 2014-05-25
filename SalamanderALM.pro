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
    Database/Tables/User.cpp \
    Database/Tables/NodeName.cpp \
    Database/Tables/NodeDescription.cpp \
    Database/Tables/NodeReferenceList.cpp \
    Database/Tables/NodeReferenceItem.cpp \
    Database/Tables/NodeReference.cpp \
    Database/Tables/NodeAttachmentList.cpp \
    Database/Tables/NodeAttachmentItem.cpp \
    Database/DataTypes/Blob.cpp \
    Database/Tables/NodeAttachment.cpp \
    Database/Tables/NodeCommentList.cpp \
    Database/Tables/NodeCommentItem.cpp \
    Database/Tables/NodeComment.cpp

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
    Database/Tables/User.h \
    Database/Tables/NodeName.h \
    Database/Tables/NodeDescription.h \
    Database/Tables/NodeReferenceList.h \
    Database/Tables/NodeReferenceItem.h \
    Database/Tables/NodeReference.h \
    Database/Tables/NodeAttachmentList.h \
    Database/Tables/NodeAttachmentItem.h \
    Database/DataTypes/Blob.h \
    Database/Tables/NodeAttachment.h \
    Database/Tables/NodeCommentList.h \
    Database/Tables/NodeCommentItem.h \
    Database/Tables/NodeComment.h

FORMS    += \
    MainWindow.ui

RESOURCES += \
    Resources/Database/Database.qrc