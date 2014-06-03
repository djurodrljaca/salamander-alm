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
#include <QtSql/QSqlRecord>
#include <QtSql/QSqlField>
#include <QtCore/QtDebug>
#include <QtCore/QFile>

#define SQLITE_PRAGMA_APPLICATION_ID qint32(0x5A1ADEA1) /* App. ID: SAlA(man)DE(r) Al(m) */
#define SQLITE_PRAGMA_ENCODING       QString("UTF-8")
#define SQLITE_PRAGMA_USER_VERSION   qint32(0) /* User version */

#define SQLITE_PRAGMA_CASE_SENSITIVE_LIKE int(0) /* Case-insensitive like */
#define SQLITE_PRAGMA_FOREIGN_KEYS        int(1) /* Enabled */
#define SQLITE_PRAGMA_LOCKING_MODE        QString("exclusive")

#define DATABASE_TYPE QString("QSQLITE")
#define DATABASE_NAME QString("database.db3")

struct PragmaItem
{
    PragmaItem()
        : name(), value()
    {}

    PragmaItem(const QString name, const QVariant value)
        : name(name), value(value)
    {}

    QString name;
    QVariant value;
};

static const PragmaItem s_persistentConfigList[] =
{
    PragmaItem(QString("application_id"), SQLITE_PRAGMA_APPLICATION_ID),
    PragmaItem(QString("encoding"),       SQLITE_PRAGMA_ENCODING),
    PragmaItem(QString("user_version"),   SQLITE_PRAGMA_USER_VERSION),
    PragmaItem()
};

static const PragmaItem s_runtimeConfigList[] =
{
    PragmaItem(QString("case_sensitive_like"), SQLITE_PRAGMA_CASE_SENSITIVE_LIKE),
    PragmaItem(QString("foreign_keys"),        SQLITE_PRAGMA_FOREIGN_KEYS),
    PragmaItem(QString("locking_mode"),        SQLITE_PRAGMA_LOCKING_MODE),
    PragmaItem()
};

using namespace Database;

SqliteDatabase::SqliteDatabase()
    : m_database()
{
    m_database = QSqlDatabase::addDatabase(DATABASE_TYPE);
}

SqliteDatabase::~SqliteDatabase()
{
    disconnect();

    const QString defaultConnectionName = m_database.connectionName();

    if (!defaultConnectionName.isEmpty())
    {
        m_database = QSqlDatabase(); // Needed to completely release the database
        QSqlDatabase::removeDatabase(defaultConnectionName);
    }
}

bool SqliteDatabase::isConnected() const
{
    return m_database.isOpen();
}

bool SqliteDatabase::connect()
{
    bool success = !isConnected();

    if (success)
    {
        m_database.setDatabaseName(DATABASE_NAME);
        success = m_database.open();

        // TODO: create database if does not exist?
    }

    if (success)
    {
        success = setRuntimeConfig();

        if (!success)
        {
            disconnect();
        }
    }

    return success;
}

void SqliteDatabase::disconnect()
{
    if (m_database.isOpen())
    {
        m_database.close();
    }
}

bool SqliteDatabase::validate() const
{
    bool success = isConnected();

    if (success)
    {
        success = integrityCheck();
    }

    if (success)
    {
        success = validatePersistentConfig();
    }

    if (success)
    {
        success = validateTables();
    }

    return success;
}

bool SqliteDatabase::create()
{
    bool initialyConnected = isConnected();

    if (initialyConnected)
    {
        disconnect();
    }

    bool success = true;

    if (success)
    {
        if (QFile::exists(DATABASE_NAME))
        {
            success = QFile::remove(DATABASE_NAME);
        }
    }

    if (success)
    {
        success = connect();
    }

    if (success)
    {
        success = setPersistentConfig();
    }

    if (success)
    {
        success = createTables();
    }

    if (success)
    {
        success = validate();
    }

    if (success)
    {
        const UserRecord user(IntegerField(),
                              UserType_Administrator,
                              TextField("Administrator"),
                              TextField("admin"),
                              TextField("admin"));

        success = addUser(user);
    }

    if (!initialyConnected)
    {
        disconnect();
    }

    return success;
}

bool SqliteDatabase::addNode(const NodeRecord &node, IntegerField *id) const
{
    // Insert value
    static const QString insertCommand(
                "INSERT INTO `Node`(`Parent`, `Type`) VALUES (:Parent, :Type);"
                );

    bool success = node.isValid();

    if (success)
    {
        QSqlQuery query;
        success = query.prepare(insertCommand);

        if (success)
        {
            // Prepare values
            QVariant parentValue = convertIntegerToVariant(node.getParent(), &success);
            QVariant typeValue;

            if (success)
            {
                const IntegerField typeIntegerValue = convertNodeTypeToInteger(node.getType(), &success);

                if (success)
                {
                    typeValue = convertIntegerToVariant(typeIntegerValue, &success);
                }
            }

            // Execute the "insert" query with the prepared values
            if (success)
            {
                query.bindValue(":Parent", parentValue);
                query.bindValue(":Type", typeValue);

                success = query.exec();
            }

            // Get Id of the inserted Node
            if (success && (id != NULL))
            {
                *id = getLastInsertId(query, &success);
            }
        }
    }

    return success;
}

NodeRecord SqliteDatabase::getNode(const IntegerField &id, bool *ok) const
{
    NodeRecord node;
    bool success = false;

    if (!id.isNull())
    {
        // Get Node from database
        static const QString selectCommand("SELECT * FROM `Node` WHERE `Id`=:Id");

        QSqlQuery query;
        success = query.prepare(selectCommand);

        if (success)
        {
            // Prepare value and execute query
            const QVariant idValue = convertIntegerToVariant(id, &success);

            if (success)
            {
                query.bindValue(":Id", idValue);

                success = query.exec();
            }

            // Get Node from executed query
            if (success)
            {
                success = query.first();

                if (success)
                {
                    node = getNodeFromQuery(query, &success);
                }
            }
        }
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return node;
}

QList<NodeRecord> SqliteDatabase::getNodes(const IntegerField &parent, bool *ok) const
{
    QList<NodeRecord> nodeList;
    bool success = false;

    // Get Node list from database
    static const QString selectCommandNull("SELECT * FROM `Node` WHERE `Parent` IS NULL");
    static const QString selectCommandValue("SELECT * FROM `Node` WHERE `Parent`=:Parent");

    QSqlQuery query;

    if (parent.isNull())
    {
        success = query.prepare(selectCommandNull);
    }
    else
    {
        success = query.prepare(selectCommandValue);

        if (success)
        {
            const QVariant parentValue = convertIntegerToVariant(parent, &success);

            if (success)
            {
                query.bindValue(":Parent", parentValue);
            }
        }
    }

    if (success)
    {
        success = query.exec();

        if (success)
        {
            while (query.next() && success)
            {
                const NodeRecord node = getNodeFromQuery(query, &success);

                if (success)
                {
                    nodeList.append(node);
                }
            }
        }
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return nodeList;
}

bool SqliteDatabase::addUser(const UserRecord &user, IntegerField *id) const
{
    // Insert value
    static const QString insertCommand(
                "INSERT INTO `User`(`Type`, `FullName`, `Username`, `Password`)"
                " VALUES (:Type, :FullName, :Username, :Password);"
                );

    bool success = user.isValid();

    if (success)
    {
        QSqlQuery query;
        success = query.prepare(insertCommand);

        if (success)
        {
            // Prepare values
            QVariant typeValue;
            QVariant fullNameValue;
            QVariant usernameValue;
            QVariant passwordValue;

            const IntegerField typeIntegerValue = convertUserTypeToInteger(user.getType(), &success);

            if (success)
            {
                typeValue = convertIntegerToVariant(typeIntegerValue, &success);
            }

            if (success)
            {
                fullNameValue = convertTextToVariant(user.getFullName(), &success);
            }

            if (success)
            {
                usernameValue = convertTextToVariant(user.getUsername(), &success);
            }

            if (success)
            {
                passwordValue = convertTextToVariant(user.getPassword(), &success);
            }

            // Execute the "insert" query with the prepared values
            if (success)
            {
                query.bindValue(":Type", typeValue);
                query.bindValue(":FullName", fullNameValue);
                query.bindValue(":Username", usernameValue);
                query.bindValue(":Password", passwordValue);

                success = query.exec();
            }

            // Get Id of the inserted User
            if (success && (id != NULL))
            {
                *id = getLastInsertId(query, &success);
            }
        }
    }

    return success;
}

UserRecord SqliteDatabase::getUser(const IntegerField &id, bool *ok) const
{
    UserRecord user;
    bool success = false;

    if (!id.isNull())
    {
        // Get User from database
        static const QString selectCommand("SELECT * FROM `User` WHERE `Id`=:Id");

        QSqlQuery query;
        success = query.prepare(selectCommand);

        if (success)
        {
            // Prepare value and execute query
            const QVariant idValue = convertIntegerToVariant(id, &success);

            if (success)
            {
                query.bindValue(":Id", idValue);

                success = query.exec();
            }

            // Get User from executed query
            if (success)
            {
                success = query.first();

                if (success)
                {
                    user = getUserFromQuery(query, &success);
                }
            }
        }
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return user;
}

QList<UserRecord> SqliteDatabase::getUsers(bool *ok) const
{
    QList<UserRecord> userList;
    bool success = false;

    // Get Node list from database
    static const QString selectCommand("SELECT * FROM `User`");

    QSqlQuery query;
    success = query.prepare(selectCommand);

    if (success)
    {
        success = query.exec();

        if (success)
        {
            while (query.next() && success)
            {
                const UserRecord node = getUserFromQuery(query, &success);

                if (success)
                {
                    userList.append(node);
                }
            }
        }
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return userList;
}

bool SqliteDatabase::integrityCheck() const
{
    const static QString command = "PRAGMA integrity_check;";
    QSqlQuery query;

    bool success = query.prepare(command);

    if (success)
    {
        success = query.exec();

        if (success)
        {
            success = query.first();

            if (success)
            {
                const QString value = query.value(0).toString();

                if (value != "ok")
                {
                    success = false;
                }
            }
        }
    }

    return success;
}

bool SqliteDatabase::validatePersistentConfig() const
{
    bool success = true;
    int index = 0;

    while (success)
    {
        // Get pragma name and value
        const PragmaItem &item = s_persistentConfigList[index];
        index++;

        if (item.name.isEmpty())
        {
            // Last item in the list, exit loop
            break;
        }

        // Get pragma value
        const QVariant value = getPragmaValue(item.name);

        // Verify pragma value
        if (value.canConvert(QVariant::String) &&
            item.value.canConvert(QVariant::String))
        {
            const QString v1 = value.toString();
            const QString v2 = item.value.toString();

            if (v1 != v2)
            {
                success = false;
            }
        }
        else
        {
            success = false;
        }
    }

    return success;
}

bool SqliteDatabase::setPersistentConfig() const
{
    bool success = true;
    int index = 0;

    while (success)
    {
        // Get pragma name and value
        const PragmaItem &item = s_persistentConfigList[index];
        index++;

        if (item.name.isEmpty())
        {
            // Last item in the list, exit loop
            break;
        }

        // Set pragma value
        success = setPragmaValue(item.name, item.value);
    }

    return success;
}

bool SqliteDatabase::setRuntimeConfig() const
{
    bool success = true;
    int index = 0;

    while (success)
    {
        // Get pragma name and value
        const PragmaItem &item = s_runtimeConfigList[index];
        index++;

        if (item.name.isEmpty())
        {
            // Last item in the list, exit loop
            break;
        }

        // Set pragma value
        success = setPragmaValue(item.name, item.value);
    }

    return success;
}

QVariant SqliteDatabase::getPragmaValue(const QString &name) const
{
    QVariant value;
    bool success = !name.isEmpty();

    if (success)
    {
        const static QString command = "PRAGMA %1;";
        QSqlQuery query;

        success = query.prepare(command.arg(name));

        if (success)
        {
            success = query.exec();

            if (success)
            {
                success = query.first();

                if (success)
                {
                    value = query.value(0);
                }
            }
        }
    }

    if (!success)
    {
        value.clear();
    }

    return value;
}

bool SqliteDatabase::setPragmaValue(const QString &name, const QVariant &value) const
{
    bool success = (!name.isEmpty() && value.isValid());

    if (success)
    {
        const static QString command = "PRAGMA %1 = '%2';";
        QSqlQuery query;

        success = query.prepare(command.arg(name, value.toString()));

        if (success)
        {
            success = query.exec();
        }
    }

    return success;
}

bool SqliteDatabase::validateTables() const
{
    // Get a list of existing tables
    QStringList existingTableList = m_database.tables();

    // Get list of needed tables
    bool success = true;
    const QStringList neededTableList = getTableList();

    foreach (const QString neededTable, neededTableList)
    {
        if (!existingTableList.contains(neededTable))
        {
            success = false;
            break;
        }
    }

    return success;
}

bool SqliteDatabase::createTables() const
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

QStringList SqliteDatabase::getTableList() const
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

bool SqliteDatabase::createTable(const QString &tableName) const
{
    // Create table
    static const QString filePath = QString(":/Database/Sqlite/Tables/%1_CreateTable.sqlite");

    QFile file(filePath.arg(tableName));

    bool success = file.open(QIODevice::ReadOnly | QIODevice::Text);

    if (success)
    {
        const QString fileContent = file.readAll();
        file.close();

        QSqlQuery query;
        success = query.exec(fileContent);
    }

    return success;
}

QVariant SqliteDatabase::convertIntegerToVariant(const IntegerField &integer, bool *ok) const
{
    QVariant value;

    if (integer.isNull())
    {
        value = QVariant(QVariant::LongLong);
    }
    else
    {
        value = QVariant(integer.getValue());
    }

    if (ok != NULL)
    {
        *ok = true;
    }

    return value;
}

IntegerField SqliteDatabase::convertVariantToInteger(const QVariant &variant, bool *ok) const
{
    IntegerField integer;
    bool success = variant.isValid();

    if (success)
    {
        if (variant.isNull())
        {
            integer.setNull();
        }
        else
        {
            switch (variant.type())
            {
                case QVariant::Int:
                case QVariant::LongLong:
                {
                    const qlonglong value = variant.toLongLong(&success);

                    if (success)
                    {
                        integer.setValue(value);
                    }
                    break;
                }

                default:
                {
                    success = false;
                    break;
                }
            }
        }
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return integer;
}

QVariant SqliteDatabase::convertTextToVariant(const TextField &text, bool *ok) const
{
    QVariant value;

    if (text.isNull())
    {
        value = QVariant(QVariant::String);
    }
    else
    {
        value = QVariant(text.getValue());
    }

    if (ok != NULL)
    {
        *ok = true;
    }

    return value;
}

TextField SqliteDatabase::convertVariantToText(const QVariant &variant, bool *ok) const
{
    TextField text;
    bool success = variant.isValid();

    if (success)
    {
        if (variant.isNull())
        {
            text.setNull();
        }
        else
        {
            switch (variant.type())
            {
                case QVariant::String:
                {
                    text.setValue(variant.toString());
                    break;
                }

                default:
                {
                    success = false;
                    break;
                }
            }
        }
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return text;
}

IntegerField SqliteDatabase::getLastInsertId(const QSqlQuery &query, bool *ok) const
{
    bool success = false;
    const IntegerField integer = convertVariantToInteger(query.lastInsertId(), &success);

    if (success && integer.isNull())
    {
        success = false;
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return integer;
}

NodeRecord SqliteDatabase::getNodeFromQuery(const QSqlQuery &query, bool *ok) const
{
    NodeRecord node;
    bool success = query.isActive();

    // Id
    if (success)
    {
        const int index = query.record().indexOf("Id");
        const IntegerField idValue = convertVariantToInteger(query.value(index), &success);

        if (success)
        {
            if (idValue.isNull())
            {
                success = false;
            }
            else
            {
                node.setId(idValue);
            }
        }
    }

    // Parent
    if (success)
    {
        const int index = query.record().indexOf("Parent");
        const IntegerField parentValue = convertVariantToInteger(query.value(index), &success);

        if (success)
        {
            node.setParent(parentValue);
        }
    }

    // Type
    if (success)
    {
        const int index = query.record().indexOf("Type");
        const IntegerField value = convertVariantToInteger(query.value(index), &success);

        if (success)
        {
            const NodeType typeValue = convertIntegerToNodeType(value, &success);

            if (success)
            {
                node.setType(typeValue);
            }
        }
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return node;
}

UserRecord SqliteDatabase::getUserFromQuery(const QSqlQuery &query, bool *ok) const
{
    UserRecord user;
    bool success = query.isActive();

    // Id
    if (success)
    {
        const int index = query.record().indexOf("Id");
        const IntegerField idValue = convertVariantToInteger(query.value(index), &success);

        if (success)
        {
            if (idValue.isNull())
            {
                success = false;
            }
            else
            {
                user.setId(idValue);
            }
        }
    }

    // Type
    if (success)
    {
        const int index = query.record().indexOf("Type");
        const IntegerField value = convertVariantToInteger(query.value(index), &success);

        if (success)
        {
            const UserType typeValue = convertIntegerToUserType(value, &success);

            if (success)
            {
                user.setType(typeValue);
            }
        }
    }

    // Full Name
    if (success)
    {
        const int index = query.record().indexOf("FullName");
        const TextField fullNameValue = convertVariantToText(query.value(index), &success);

        if (success)
        {
            user.setFullName(fullNameValue);
        }
    }

    // Username
    if (success)
    {
        const int index = query.record().indexOf("Username");
        const TextField usernameValue = convertVariantToText(query.value(index), &success);

        if (success)
        {
            user.setUsername(usernameValue);
        }
    }

    // Password
    if (success)
    {
        const int index = query.record().indexOf("Password");
        const TextField passwordValue = convertVariantToText(query.value(index), &success);

        if (success)
        {
            user.setPassword(passwordValue);
        }
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return user;
}
