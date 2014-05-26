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

#include "Database/DataTypes/Integer.h"
#include "Database/DataTypes/Boolean.h"
#include "Database/Tables/Node.h"
#include "Database/Tables/NodeType.h"
#include "Database/Tables/NodeAttributes.h"
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

    bool addNode(const DataTypes::Integer &parent,
                 const DataTypes::Integer &type,
                 DataTypes::Integer *id = NULL) const;
    Tables::Node getNode(const DataTypes::Integer &id, bool *ok = NULL) const;
    QList<Tables::Node> getNodes(const DataTypes::Integer &parent, bool *ok = NULL) const;

    Tables::NodeType getNodeType(const DataTypes::Integer &id, bool *ok = NULL) const;

    bool addNodeAttributes(const DataTypes::Integer &node,
                           const DataTypes::Integer &revision,
                           const DataTypes::Integer &name,
                           const DataTypes::Integer &description,
                           const DataTypes::Integer &references,
                           const DataTypes::Integer &attachments,
                           const DataTypes::Integer &comments,
                           const DataTypes::Boolean &isActive,
                           DataTypes::Integer *id = NULL) const;









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
    bool executeScriptFile(const QString &scriptFilePath) const;

    DataTypes::Integer getLastInsertId(const QSqlQuery &query, bool *ok = NULL) const;

    DataTypes::Integer convertVariantToInteger(const QVariant &value, bool *ok = NULL) const;
    DataTypes::Text convertVariantToText(const QVariant &value, bool *ok = NULL) const;

    Tables::Node getNodeFromQuery(const QSqlQuery &query, bool *ok = NULL) const;

    QSqlDatabase m_database;
};
}

#endif // SQLITEDATABASE_H
