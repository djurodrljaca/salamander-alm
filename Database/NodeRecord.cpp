/**
 * @file   Node.cpp
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

#include "Database/NodeRecord.h"
#include <QtCore/QString>

using namespace Database;

NodeRecord::NodeRecord()
    : m_id(),
      m_parent(),
      m_type(NodeType_Invalid)
{
}

NodeRecord::NodeRecord(const IntegerField &id,
                       const IntegerField &parent,
                       const NodeType type)
    : m_id(id),
      m_parent(parent),
      m_type(type)
{
}

bool NodeRecord::isValid() const
{
    return isNodeTypeValid(m_type);
}

IntegerField NodeRecord::getId() const
{
    return m_id;
}

void NodeRecord::setId(const IntegerField &id)
{
    m_id = id;
}

IntegerField NodeRecord::getParent() const
{
    return m_parent;
}

void NodeRecord::setParent(const IntegerField &parent)
{
    m_parent = parent;
}

NodeType NodeRecord::getType() const
{
    return m_type;
}

void NodeRecord::setType(const NodeType type)
{
    m_type = type;
}

QDebug operator<<(QDebug dbg, const NodeRecord &node)
{
    dbg.nospace() << "< NodeRecord: Id=" << node.getId();
    dbg.nospace() << "Parent="<< node.getParent();
    dbg.nospace() << "Type=" << node.getType() << ">";

    return dbg.space();
}
