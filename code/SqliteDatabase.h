/**
 * @file   SqliteDatabase.h
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

#ifndef SQLITEDATABASE_H
#define SQLITEDATABASE_H

#include <QtCore/QStringList>
#include <QtSql/QSqlDatabase>

class SqliteDatabase
{
public:
    SqliteDatabase();
    ~SqliteDatabase();

    bool connect();
    void disconnect();

private:
    bool init();
    bool createTables();
    QStringList getTableList();
    bool createTable(const QString &tableName);
    bool executeScriptFile(const QString &scriptFilePath);

    QSqlDatabase m_database;
};

#endif // SQLITEDATABASE_H
