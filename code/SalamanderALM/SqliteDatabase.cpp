/**
 * @file   SqliteDatabase.cpp
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-5-24
 * @brief  Brief description of file.
 *
 * Copyright 2014  Djuro Drljaca (djurodrljaca@gmail.com)
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "SqliteDatabase.h"
#include <QtSql/QSqlQuery>
#include <QtSql/QSqlError>
#include <QtSql/QSqlResult>
#include <QtCore/QtDebug>
#include <QtCore/QFile>

SqliteDatabase::SqliteDatabase()
    : m_database()
{
    m_database = QSqlDatabase::addDatabase("QSQLITE");
}

SqliteDatabase::~SqliteDatabase()
{
    m_database.removeDatabase("SalamanderALM");
}

bool SqliteDatabase::open()
{
    m_database.setDatabaseName("SalamanderALM.db3");
    bool success = m_database.open();

    if (success)
    {
        success = init();

        if (!success)
        {
            close();
        }
    }

    return success;
}

void SqliteDatabase::close()
{
    if (m_database.isOpen())
    {
        m_database.close();
    }
}

bool SqliteDatabase::init()
{
    QSqlQuery query;

    bool success = query.exec("PRAGMA foreign_keys = ON;");

    if (success)
    {
        success = createTables();
    }

    return success;
}

bool SqliteDatabase::createTables()
{
    bool success = false;
    const QStringList tableList = getTableList();

    if (tableList.size() > 0)
    {
        success = true;

        foreach (const QString tableName, tableList)
        {
            if (!createTable(tableName))
            {
                success = false;
                break;
            }
        }
    }

    return success;
}

QStringList SqliteDatabase::getTableList()
{
    QFile file(":/Database/Sqlite/Tables/Tables.txt");

    QStringList tableList;
    bool success = file.open(QIODevice::ReadOnly | QIODevice::Text);

    if (success)
    {
        const QString fileContent = file.readAll();
        file.close();

        tableList = fileContent.split(QRegExp("\\s"), QString::SkipEmptyParts);
    }

    return tableList;
}

bool SqliteDatabase::createTable(const QString &tableName)
{
    // Check if table exists
    const QString queryCommand =
            QString("SELECT name FROM sqlite_master WHERE type='%1'").arg(tableName);

    QSqlQuery query;
    bool success = query.exec(queryCommand);
    bool tableExists = false;

    if (success)
    {
        const int size = query.size();
        tableExists = (size == 1);
    }

    // Create table
    if (success && !tableExists)
    {
        const QString filePath =
                QString(":/Database/Sqlite/Tables/CreateTable_%1.sqlite").arg(tableName);
        success = executeScriptFile(filePath);
    }

    return success;
}

bool SqliteDatabase::executeScriptFile(const QString &scriptFilePath)
{
    QFile file(scriptFilePath);

    bool success = file.open(QIODevice::ReadOnly | QIODevice::Text);

    if (success)
    {
        const QString fileContent = file.readAll();
        file.close();

        const QStringList queryList = fileContent.split(QRegExp(";\\s"), QString::SkipEmptyParts);

        foreach (const QString queryCommand, queryList)
        {
            QSqlQuery query;

            bool success = query.exec(queryCommand);

            if (!success)
            {
                break;
            }
        }
    }

    return success;
}
