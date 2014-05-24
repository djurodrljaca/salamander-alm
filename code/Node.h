/**
 * @file   Node.h
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

#ifndef NODE_H
#define NODE_H

#include "Id.h"
#include <QtSql/QSqlRecord>

namespace Database
{
class Node
{
public:
    Node();
    Node(const Id id, const Id parent, const Id type);

    bool isValid() const;

    Id getId() const;
    void setId(const Id id);

    Id getParent() const;
    void setParent(const Id parent);

    Id getType() const;
    void setType(const Id type);

    static Node fromRecord(const QSqlRecord &record, bool *ok = NULL);

private:
    Id m_id;
    Id m_parent;
    Id m_type;
};
}

#endif // NODE_H
