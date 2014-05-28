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

Node::Node()
    : m_id(),
      m_type(Database::NodeType_Invalid),
      m_parent(NULL),
      m_childList()
{
}

Node::Node(const Node &other)
    : m_id(other.m_id),
      m_type(other.m_type),
      m_parent(other.m_parent),
      m_childList(other.m_childList)
{
}

Node::~Node()
{
    qDeleteAll(m_childList);
}

Node & Node::operator =(const Node &other)
{
    m_id = other.m_id;
    m_type = other.m_type;
    m_parent = other.m_parent;
    m_childList = other.m_childList;

    return *this;
}

bool Node::isValid() const
{
    return Database::isNodeTypeValid(m_type);
}

Database::IntegerField Node::getId() const
{
    return m_id;
}

void Node::setId(const Database::IntegerField &id)
{
    m_id = id;
}

Database::NodeType Node::getType() const
{
    return m_type;
}

void Node::setType(const Database::NodeType type)
{
    m_type = type;
}

Node * Node::getParent() const
{
    return m_parent;
}

void Node::setParent(Node *parent)
{
    m_parent = parent;
}

int Node::getChildCount() const
{
    return m_childList.size();
}

Node * Node::getChild(const int index)
{
    Node *child = NULL;

    if ((index >= 0) && (index < m_childList.size()))
    {
        child = m_childList[index];
    }

    return child;
}

int Node::getChildIndex(Node * const child) const
{
    return m_childList.indexOf(child);
}

bool Node::addChild(Node *child)
{
    bool success = false;

    if (child != NULL)
    {
        m_childList.append(child);
    }

    return success;
}
