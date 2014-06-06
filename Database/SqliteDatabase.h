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

#include "Database/NodeRecord.h"
#include "Database/UserRecord.h"
#include "Database/RevisionRecord.h"
#include "Database/NodeNameRecord.h"
#include "Database/NodeDescriptionRecord.h"
#include "Database/NodeAttributesRecord.h"
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

    IntegerField startRevision(bool *ok = NULL);
    bool finishRevision();
    void abortRevision();

    bool addNode(const NodeRecord &node, IntegerField *id = NULL) const;
    NodeRecord getNode(const IntegerField &id, bool *ok = NULL) const;
    QList<NodeRecord> getNodes(const IntegerField &parent, bool *ok = NULL) const;

    bool addUser(const UserRecord &user, IntegerField *id = NULL) const;
    UserRecord getUser(const IntegerField &id, bool *ok = NULL) const;
    QList<UserRecord> getUsers(bool *ok = NULL) const;

    bool addRevision(const RevisionRecord &revision) const;
    RevisionRecord getRevision(const IntegerField &id, bool *ok = NULL) const;
    IntegerField getCurrentRevisionId(bool *ok = NULL) const;

    bool addNodeName(const NodeNameRecord &nodeName, IntegerField *id = NULL) const;
    NodeNameRecord getNodeName(const IntegerField &id, bool *ok = NULL) const;

    bool addNodeDescription(const NodeDescriptionRecord &nodeDescription,
                            IntegerField *id = NULL) const;
    NodeDescriptionRecord getNodeDescription(const IntegerField &id, bool *ok = NULL) const;

    bool addNodeAttributes(const NodeAttributesRecord &nodeAttributes,
                           IntegerField *id = NULL) const;
    NodeAttributesRecord getNodeAttributes(const IntegerField &id, bool *ok = NULL) const;
    IntegerField getNodeAttributesId(const IntegerField &nodeId,
                                     const IntegerField &revisionId,
                                     bool *ok = NULL) const;

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

    QVariant convertBooleanToVariant(const BooleanField &boolean, bool *ok = NULL) const;
    BooleanField convertVariantToBoolean(const QVariant &variant, bool *ok = NULL) const;

    QVariant convertDateTimeToVariant(const DateTimeField &dateTime, bool *ok = NULL) const;
    DateTimeField convertVariantToDateTime(const QVariant &variant, bool *ok = NULL) const;

    QVariant convertIntegerToVariant(const IntegerField &integer, bool *ok = NULL) const;
    IntegerField convertVariantToInteger(const QVariant &variant, bool *ok = NULL) const;

    QVariant convertTextToVariant(const TextField &text, bool *ok = NULL) const;
    TextField convertVariantToText(const QVariant &variant, bool *ok = NULL) const;

    IntegerField getLastInsertId(const QSqlQuery &query, bool *ok = NULL) const;

    NodeRecord getNodeFromQuery(const QSqlQuery &query, bool *ok = NULL) const;
    UserRecord getUserFromQuery(const QSqlQuery &query, bool *ok = NULL) const;
    RevisionRecord getRevisionFromQuery(const QSqlQuery &query, bool *ok = NULL) const;
    NodeNameRecord getNodeNameFromQuery(const QSqlQuery &query, bool *ok = NULL) const;
    NodeDescriptionRecord getNodeDescriptionFromQuery(const QSqlQuery &query, bool *ok = NULL) const;
    NodeAttributesRecord getNodeAttributesFromQuery(const QSqlQuery &query, bool *ok = NULL) const;

    QSqlDatabase m_database;
};
}

#endif // DATABASE_SQLITEDATABASE_H
