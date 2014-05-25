/**
 * @file   NodeReference.h
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-05-25
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

#ifndef DATABASE_TABLES_NODEREFERENCE_H
#define DATABASE_TABLES_NODEREFERENCE_H

#include "Database/DataTypes/Boolean.h"
#include "Database/DataTypes/Integer.h"
#include <QtSql/QSqlRecord>

namespace Database
{
namespace Tables
{
class NodeReference
{
public:
    NodeReference();
    NodeReference(const DataTypes::Integer &id,
                   const DataTypes::Integer &node);

    bool isValid() const;

    DataTypes::Integer getId() const;
    void setId(const DataTypes::Integer &id);

    DataTypes::Integer getNode() const;
    void setNode(const DataTypes::Integer &node);

    static NodeReference fromRecord(const QSqlRecord &record, bool *ok = NULL);

private:
    DataTypes::Integer m_id;
    DataTypes::Integer m_node;
};
}
}

#endif // DATABASE_TABLES_NODEREFERENCE_H
