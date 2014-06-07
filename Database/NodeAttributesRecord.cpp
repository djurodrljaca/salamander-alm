/**
 * @file   NodeAttributesRecord.cpp
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

#include "Database/NodeAttributesRecord.h"
#include <QtCore/QString>

using namespace Database;

NodeAttributesRecord::NodeAttributesRecord()
    : m_id(),
      m_node(),
      m_revision(),
      m_name(),
      m_description(),
      m_references(),
      m_attachments(),
      m_comments(),
      m_active()
{
}

NodeAttributesRecord::NodeAttributesRecord(const IntegerField &id,
                                           const IntegerField &node,
                                           const IntegerField &revision,
                                           const IntegerField &name,
                                           const IntegerField &description,
                                           const IntegerField &references,
                                           const IntegerField &attachments,
                                           const IntegerField &comments,
                                           const BooleanField &active)
    : m_id(id),
      m_node(node),
      m_revision(revision),
      m_name(name),
      m_description(description),
      m_references(references),
      m_attachments(attachments),
      m_comments(comments),
      m_active(active)
{
}

bool NodeAttributesRecord::isValid() const
{
    return (!m_node.isNull() &&
            !m_revision.isNull() &&
            !m_name.isNull() &&
            !m_active.isNull());
}

IntegerField NodeAttributesRecord::getId() const
{
    return m_id;
}

void NodeAttributesRecord::setId(const IntegerField &id)
{
    m_id = id;
}

IntegerField NodeAttributesRecord::getNode() const
{
    return m_node;
}

void NodeAttributesRecord::setNode(const IntegerField &node)
{
    m_node = node;
}

IntegerField NodeAttributesRecord::getRevision() const
{
    return m_revision;
}

void NodeAttributesRecord::setRevision(const IntegerField &revision)
{
    m_revision = revision;
}

IntegerField NodeAttributesRecord::getName() const
{
    return m_name;
}

void NodeAttributesRecord::setName(const IntegerField &name)
{
    m_name = name;
}

IntegerField NodeAttributesRecord::getDescription() const
{
    return m_description;
}

void NodeAttributesRecord::setDescription(const IntegerField &description)
{
    m_description = description;
}

IntegerField NodeAttributesRecord::getReferences() const
{
    return m_references;
}

void NodeAttributesRecord::setReferences(const IntegerField &references)
{
    m_references = references;
}

IntegerField NodeAttributesRecord::getAttachments() const
{
    return m_attachments;
}

void NodeAttributesRecord::setAttachments(const IntegerField &attachments)
{
    m_attachments = attachments;
}

IntegerField NodeAttributesRecord::getComments() const
{
    return m_comments;
}

void NodeAttributesRecord::setComments(const IntegerField &comments)
{
    m_comments = comments;
}

BooleanField NodeAttributesRecord::getActive() const
{
    return m_active;
}

void NodeAttributesRecord::setActive(const BooleanField &active)
{
    m_active = active;
}

QDebug operator<<(QDebug dbg, const NodeAttributesRecord &nodeAttributes)
{
    dbg.nospace() << "< NodeAttributesRecord: Id=" << nodeAttributes.getId();
    dbg.nospace() << "Node="<< nodeAttributes.getNode();
    dbg.nospace() << "Revision="<< nodeAttributes.getRevision();
    dbg.nospace() << "Name="<< nodeAttributes.getName();
    dbg.nospace() << "Description="<< nodeAttributes.getDescription();
    dbg.nospace() << "References="<< nodeAttributes.getReferences();
    dbg.nospace() << "Attachments="<< nodeAttributes.getAttachments();
    dbg.nospace() << "Comments="<< nodeAttributes.getComments();
    dbg.nospace() << "Active=" << nodeAttributes.getActive() << ">";

    return dbg.space();
}
