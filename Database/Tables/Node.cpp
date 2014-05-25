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

#include "Database/Tables/Node.h"

using namespace Database::Tables;
using namespace Database::DataTypes;

Node::Node()
    : m_id(),
      m_parent(),
      m_type()
{
}

Node::Node(const Integer &id,
           const Integer &parent,
           const Integer &type)
    : m_id(id),
      m_parent(parent),
      m_type(type)
{
}

bool Node::isValid() const
{
    return (!m_id.isNull() &&
            !m_type.isNull());
}

Integer Node::getId() const
{
    return m_id;
}

void Node::setId(const Integer &id)
{
    m_id = id;
}

Integer Node::getParent() const
{
    return m_parent;
}

void Node::setParent(const Integer &parent)
{
    m_parent = parent;
}

Integer Node::getType() const
{
    return m_type;
}

void Node::setType(const Integer &type)
{
    m_type = type;
}

QString Node::toString() const
{
    static const QString str("Node (Id='%1' Parent='%2' Type='%3')");

    return str.arg(m_id.toString(),
                   m_parent.toString(),
                   m_type.toString());
}
