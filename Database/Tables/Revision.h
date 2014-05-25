/**
 * @file   Revision.h
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-5-25
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

#ifndef DATABASE_TABLES_REVISION_H
#define DATABASE_TABLES_REVISION_H

#include "Database/DataTypes/Integer.h"
#include "Database/DataTypes/DateTime.h"
#include <QtSql/QSqlRecord>

namespace Database
{
namespace Tables
{
class Revision
{
public:
    Revision();
    Revision(const DataTypes::Integer &id,
             const DataTypes::DateTime &timestamp,
             const DataTypes::Integer &user);

    bool isValid() const;

    DataTypes::Integer getId() const;
    void setId(const DataTypes::Integer &id);

    DataTypes::DateTime getTimestamp() const;
    void setTimestamp(const DataTypes::DateTime &timestamp);

    DataTypes::Integer getUser() const;
    void setUser(const DataTypes::Integer &user);

    static Revision fromRecord(const QSqlRecord &record, bool *ok = NULL);

private:
    DataTypes::Integer m_id;
    DataTypes::DateTime m_timestamp;
    DataTypes::Integer m_user;
};
}
}

#endif // DATABASE_TABLES_REVISION_H
