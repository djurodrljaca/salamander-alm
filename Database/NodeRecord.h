/**
 * @file   NodeRecord.h
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

#ifndef DATABASE_NODERECORD_H
#define DATABASE_NODERECORD_H

#include "Database/IntegerField.h"
#include "Database/NodeType.h"
#include <QtCore/QtDebug>

namespace Database
{
class NodeRecord
{
public:
    NodeRecord();
    NodeRecord(const IntegerField &id,
               const IntegerField &parent,
               const NodeType type);

    bool isValid() const;

    IntegerField getId() const;
    void setId(const IntegerField &id);

    IntegerField getParent() const;
    void setParent(const IntegerField &parent);

    NodeType getType() const;
    void setType(const NodeType type);

private:
    IntegerField m_id;
    IntegerField m_parent;
    NodeType m_type;
};
}

QDebug operator<<(QDebug dbg, const Database::NodeRecord &node);

#endif // DATABASE_NODERECORD_H
