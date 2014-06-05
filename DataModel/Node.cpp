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
      m_parent(NULL),
      m_type(Database::NodeType_Invalid),
      m_revisionId(),
      m_name(),
      m_descriptionId(),
      m_referencesId(),
      m_attachmentsId(),
      m_commentsId(),
      m_childList()
{
}

Node::~Node()
{
    qDeleteAll(m_childList);
}

bool Node::isValid() const
{
    return (Database::isNodeTypeValid(m_type) &&
            !m_revisionId.isNull() &&
            !m_name.isEmpty());
}

Database::IntegerField Node::getId() const
{
    return m_id;
}

void Node::setId(const Database::IntegerField &id)
{
    m_id = id;
}

Node * Node::getParent() const
{
    return m_parent;
}

void Node::setParent(Node *parent)
{
    m_parent = parent;
}

Database::NodeType Node::getType() const
{
    return m_type;
}

void Node::setType(const Database::NodeType type)
{
    m_type = type;
}

Database::IntegerField Node::getRevisionId() const
{
    return m_revisionId;
}

void Node::setRevisionId(const Database::IntegerField &revisionId)
{
    m_revisionId = revisionId;
}

QString Node::getName() const
{
    return m_name;
}

void Node::setName(const QString &name)
{
    m_name = name;
}

Database::IntegerField Node::getDescriptionId() const
{
    return m_descriptionId;
}

void Node::setDescriptionId(const Database::IntegerField &descriptionId)
{
    m_descriptionId = descriptionId;
}

Database::IntegerField Node::getReferencesId() const
{
    return m_referencesId;
}

void Node::setReferencesId(const Database::IntegerField &referencesId)
{
    m_referencesId = referencesId;
}

Database::IntegerField Node::getAttachmentsId() const
{
    return m_attachmentsId;
}

void Node::setAttachmentsId(const Database::IntegerField &attachmentsId)
{
    m_attachmentsId = attachmentsId;
}

Database::IntegerField Node::getCommentsId() const
{
    return m_commentsId;
}

void Node::setCommentsId(const Database::IntegerField &commentsId)
{
    m_commentsId = commentsId;
}

int Node::getChildCount() const
{
    return m_childList.size();
}

Node * Node::getChild(const int index) const
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
        success = true;
    }

    return success;
}
