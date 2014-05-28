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

#ifndef DATABASE_SQLITEDATABASE_H
#define DATABASE_SQLITEDATABASE_H

#include "Database/IntegerField.h"
#include "Database/NodeRecord.h"
#include <QtCore/QList>
#include <QtCore/QStringList>
#include <QtSql/QSqlDatabase>

namespace Database
{
class SqliteDatabase
{
public:
    SqliteDatabase();
    ~SqliteDatabase();

    bool isConnected() const;
    bool connect();
    void disconnect();

    bool validate() const;
    bool create();

    bool addNode(const NodeRecord &node, IntegerField *id = NULL) const;
    NodeRecord getNode(const IntegerField &id, bool *ok = NULL) const;
    QList<NodeRecord> getNodes(const IntegerField &parent, bool *ok = NULL) const;








private:
    bool integrityCheck() const;
    bool validatePersistentConfig() const;
    bool setPersistentConfig() const;
    bool setRuntimeConfig() const;

    QVariant getPragmaValue(const QString &name) const;
    bool setPragmaValue(const QString &name, const QVariant &value) const;

    bool validateTables() const;
    bool createTables() const;
    QStringList getTableList() const;
    bool createTable(const QString &tableName) const;

    QVariant convertIntegerToVariant(const IntegerField &integer, bool *ok = NULL) const;
    IntegerField convertVariantToInteger(const QVariant &variant, bool *ok = NULL) const;

    IntegerField getLastInsertId(const QSqlQuery &query, bool *ok = NULL) const;

//    DataTypes::Text convertVariantToText(const QVariant &value, bool *ok = NULL) const;

    NodeRecord getNodeFromQuery(const QSqlQuery &query, bool *ok = NULL) const;

    QSqlDatabase m_database;
};
}

#endif // DATABASE_SQLITEDATABASE_H
