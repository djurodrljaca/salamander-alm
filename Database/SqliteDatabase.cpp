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
using namespace Database::DataTypes;
using namespace Database::Tables;

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

    if (!initialyConnected)
    {
        disconnect();
    }

    return success;
}

bool SqliteDatabase::addNode(const Integer &parent, const Integer &type, Integer *id) const
{
    // Insert value
    static const QString insertCommand(
                "INSERT INTO `Node`(`Parent`, `Type`) VALUES (:Parent, :Type);"
                );

    bool success = !type.isNull();

    if (success)
    {
        QSqlQuery query;
        success = query.prepare(insertCommand);

        if (success)
        {
            query.bindValue(":Parent", parent.toVariant());
            query.bindValue(":Type", type.toVariant());

            success = query.exec();
        }
    }

    // Get Node.Id
    if (success && (id != NULL))
    {
        QSqlQuery query;
        success = query.exec("SELECT last_insert_rowid();");

        if (success)
        {
            success = query.first();

            if (success)
            {
                *id = convertVariantToInteger(query.value(0), &success);

                if (success && id->isNull())
                {
                    success = false;
                }
            }
        }
    }

    return success;
}

Node SqliteDatabase::getNode(const Integer &id, bool *ok) const
{
    Node node;
    bool success = false;

    if (!id.isNull())
    {
        // Get Node from database
        static const QString selectCommand(
                    "SELECT `Parent`,`Type`"
                    " FROM `Node`"
                    " WHERE `Id`=:Id"
                    );

        QSqlQuery query;
        success = query.prepare(selectCommand);

        if (success)
        {
            query.bindValue(":Id", id.toVariant());

            success = query.exec();

            if (success)
            {
                success = query.first();
            }
        }

        // Id
        if (success)
        {
            node.setId(id);
        }

        // Parent
        if (success)
        {
            const Integer value = convertVariantToInteger(query.value(0), &success);

            if (success)
            {
                node.setParent(value);
            }
        }

        // Type
        if (success)
        {
            const Integer value = convertVariantToInteger(query.value(1), &success);

            if (success)
            {
                if (value.isNull())
                {
                    success = false;
                }
                else
                {
                    node.setType(value);
                }
            }
        }
    }

    if (!success || !node.isValid())
    {
        node = Node();
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return node;
}

NodeType SqliteDatabase::getNodeType(const Integer &id, bool *ok) const
{
    NodeType nodeType;
    bool success = false;

    if (!id.isNull())
    {
        // Get NodeType from database
        static const QString selectCommand(
                    "SELECT `Name`"
                    " FROM `NodeType`"
                    " WHERE `Id`=:Id"
                    );

        QSqlQuery query;
        success = query.prepare(selectCommand);

        if (success)
        {
            query.bindValue(":Id", id.toVariant());

            success = query.exec();

            if (success)
            {
                success = query.first();
            }
        }

        // Id
        if (success)
        {
            nodeType.setId(id);
        }

        // Name
        if (success)
        {
            const Text value = convertVariantToText(query.value(0), &success);

            if (success)
            {
                nodeType.setName(value);
            }
        }
    }

    if (!success || !nodeType.isValid())
    {
        nodeType = NodeType();
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return nodeType;
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
                qDebug() << "SqliteDatabase::validatePersistentConfig: invalid values:" << v1 << v2;
                success = false;
            }
        }
        else
        {
            qDebug() << "SqliteDatabase::validatePersistentConfig: invalid types:" << value << item.value;
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
    const QString filePath =
            QString(":/Database/Sqlite/Tables/%1_CreateTable.sqlite").arg(tableName);

    return executeScriptFile(filePath);
}

bool SqliteDatabase::executeScriptFile(const QString &scriptFilePath) const
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

Integer SqliteDatabase::convertVariantToInteger(const QVariant &value, bool *ok) const
{
    Integer integerValue;
    bool success = value.isValid();

    if (success)
    {
        if (value.isNull())
        {
            integerValue.setNull();
        }
        else
        {
            switch (value.type())
            {
                case QVariant::Int:
                case QVariant::LongLong:
                {
                    const qint64 newValue = value.toLongLong(&success);

                    if (success)
                    {
                        integerValue.setValue(newValue);
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

    return integerValue;
}

Text SqliteDatabase::convertVariantToText(const QVariant &value, bool *ok) const
{
    Text textValue;
    bool success = value.isValid();

    if (success)
    {
        if (value.isNull())
        {
            textValue.setNull();
        }
        else
        {
            if (value.type() == QVariant::String)
            {
                textValue.setValue(value.toString());
            }
        }
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return textValue;
}
