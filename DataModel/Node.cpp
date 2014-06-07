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
      m_nameChanged(false),
      m_description(),
      m_descriptionChanged(false),
      m_active(false),
      m_activeChanged(false)
{
}

Node::Node(const IntegerField &id,
           const NodeType type,
           const QString &name,
           const QString &description,
           const bool active)
    : m_id(id),
      m_type(type),
      m_name(name),
      m_nameChanged(false),
      m_description(description),
      m_descriptionChanged(false),
      m_active(active),
      m_activeChanged(false)
{
}

void Node::clear()
{
    m_id = IntegerField();
    m_type = NodeType_Invalid;
    m_name = QString();
    m_nameChanged = false;
    m_description = QString();
    m_descriptionChanged = false;
    m_active = false;
    m_activeChanged = false;
}

bool Node::isValid() const
{
    return (!m_id.isNull() &&
            isNodeTypeValid(m_type) &&
            !m_name.isEmpty());
}

bool Node::hasChanged() const
{
    return (m_nameChanged ||
            m_descriptionChanged ||
            m_activeChanged);
}

void Node::acceptChanges()
{
    m_nameChanged = false;
    m_descriptionChanged = false;
    m_activeChanged = false;
}

IntegerField Node::getId() const
{
    return m_id;
}

NodeType Node::getType() const
{
    return m_type;
}

QString Node::getName() const
{
    return m_name;
}

void Node::setName(const QString &name)
{
    if (m_name != name)
    {
        m_name = name;
        m_nameChanged = true;
    }
}

bool Node::nameChanged() const
{
    return m_nameChanged;
}

QString Node::getDescription() const
{
    return m_description;
}

void Node::setDescription(const QString &description)
{
    if (m_description != description)
    {
        m_description = description;
        m_descriptionChanged = true;
    }
}

bool Node::descriptionChanged() const
{
    return m_descriptionChanged;
}

bool Node::getActive() const
{
    return m_active;
}

void Node::setActive(const bool active)
{
    if (m_active != active)
    {
        m_active = active;
        m_activeChanged = true;
    }
}

bool Node::activeChanged() const
{
    return m_activeChanged;
}
