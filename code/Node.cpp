/**
 * @file   Node.cpp
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

#include "Node.h"

using namespace Database;

Node::Node()
    : m_id(),
      m_parent(),
      m_type()
{
}

Node::Node(const Id id, const Id parent, const Id type)
    : m_id(id),
      m_parent(parent),
      m_type(type)
{
}

bool Node::isValid() const
{
    return (m_id.isNull() || m_type.isNull());
}

Id Node::getId() const
{
    return m_id;
}

void Node::setId(const Id id)
{
    m_id = id;
}

Id Node::getParent() const
{
    return m_parent;
}

void Node::setParent(const Id parent)
{
    m_parent = parent;
}

Id Node::getType() const
{
    return m_type;
}

void Node::setType(const Id type)
{
    m_type = type;
}

Node Node::fromRecord(const QSqlRecord &record, bool *ok)
{
    Node node;
    bool success = !record.isEmpty();

    // Id
    if (success)
    {
        node.setId(Id::fromField(record.field("Id"), &success));
    }

    // Parent
    if (success)
    {
        node.setParent(Id::fromField(record.field("Parent"), &success));
    }

    // Type
    if (success)
    {
        node.setParent(Id::fromField(record.field("Type"), &success));
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return node;
}
