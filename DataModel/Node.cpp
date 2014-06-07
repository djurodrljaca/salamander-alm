/**
 * @file   Node.cpp
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-05-27
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

#include "DataModel/Node.h"

using namespace DataModel;
using namespace Database;

Node::Node()
    : m_id(),
      m_type(NodeType_Invalid),
      m_name(),
      m_description()
{
}

bool Node::isValid() const
{
    return (!m_id.isNull() &&
            isNodeTypeValid(m_type) &&
            !m_name.isEmpty());
}

IntegerField Node::getId() const
{
    return m_id;
}

void Node::setId(const IntegerField &id)
{
    m_id = id;
}

NodeType Node::getType() const
{
    return m_type;
}

void Node::setType(const NodeType type)
{
    m_type = type;
}

QString Node::getName() const
{
    return m_name;
}

void Node::setName(const QString &name)
{
    m_name = name;
}

QString Node::getDescription() const
{
    return m_description;
}

void Node::setDescription(const QString &description)
{
    m_description = description;
}
