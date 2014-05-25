/**
 * @file   Node.h
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-05-24
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

#ifndef DATABASE_TABLES_NODE_H
#define DATABASE_TABLES_NODE_H

#include "Database/DataTypes/Integer.h"
#include <QtSql/QSqlRecord>
#include <QtCore/QString>

namespace Database
{
namespace Tables
{
class Node
{
public:
    Node();
    Node(const DataTypes::Integer &id,
         const DataTypes::Integer &parent,
         const DataTypes::Integer &type);

    bool isValid() const;

    DataTypes::Integer getId() const;
    void setId(const DataTypes::Integer &id);

    DataTypes::Integer getParent() const;
    void setParent(const DataTypes::Integer &parent);

    DataTypes::Integer getType() const;
    void setType(const DataTypes::Integer &type);

    QString toString() const;

private:
    DataTypes::Integer m_id;
    DataTypes::Integer m_parent;
    DataTypes::Integer m_type;
};
}
}

#endif // DATABASE_TABLES_NODE_H
