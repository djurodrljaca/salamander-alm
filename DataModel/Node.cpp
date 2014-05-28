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
      m_children()
{
}

Node::Node(const Node &other)
    : m_id(other.m_id),
      m_type(other.m_type),
      m_parent(NULL),
      m_children(other.m_children)
{
    if (other.m_parent != NULL)
    {
        m_parent = new Node(*other.m_parent);
    }
}

Node::~Node()
{
    delete m_parent;
}

Node &Node::operator=(const Node &other)
{
    m_id = other.m_id;
    m_type = other.m_type;
    m_children = other.m_children;

    if (other.m_parent != NULL)
    {
        m_parent = new Node(*other.m_parent);
    }

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

Node *Node::getParent() const
{
    return m_parent;
}

void Node::setParent(const Node *parent)
{
    delete m_parent;

    if (parent == NULL)
    {
        m_parent = NULL;
    }
    else
    {
        m_parent = new Node(*parent);
    }
}

int Node::getChildrenCount() const
{
    return m_children.size();
}

bool Node::addChild(const Node &child)
{
    m_children.append(child);
    return true;
}

Node * Node::getChild(const int index)
{
    Node *node = NULL;

    if ((index >= 0) && (index < m_children.size()))
    {
        node = &m_children[index];
    }

    return node;
}
