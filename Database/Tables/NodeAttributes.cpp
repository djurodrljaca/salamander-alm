/**
 * @file   NodeAttributes.cpp
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-05-25
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

#include "Database/Tables/NodeAttributes.h"

using namespace Database::Tables;
using namespace Database::DataTypes;

NodeAttributes::NodeAttributes()
    : m_id(),
      m_node(),
      m_revision(),
      m_name(),
      m_description(),
      m_references(),
      m_attachments(),
      m_comments(),
      m_isActive()
{
}

NodeAttributes::NodeAttributes(const Integer &id,
                               const Integer &node,
                               const Integer &revision,
                               const Integer &name,
                               const Integer &description,
                               const Integer &references,
                               const Integer &attachments,
                               const Integer &comments,
                               const Boolean &isActive)
    : m_id(id),
      m_node(node),
      m_revision(revision),
      m_name(name),
      m_description(description),
      m_references(references),
      m_attachments(attachments),
      m_comments(comments),
      m_isActive(isActive)
{
}

bool NodeAttributes::isValid() const
{
    return (!m_id.isNull() &&
            !m_node.isNull() &&
            !m_revision.isNull() &&
            !m_name.isNull() &&
            !m_isActive.isNull());
}

Integer NodeAttributes::getId() const
{
    return m_id;
}

void NodeAttributes::setId(const Integer &id)
{
    m_id = id;
}

Integer NodeAttributes::getNode() const
{
    return m_node;
}

void NodeAttributes::setNode(const Integer &node)
{
    m_node = node;
}

Integer NodeAttributes::getRevision() const
{
    return m_revision;
}

void NodeAttributes::setRevision(const Integer &revision)
{
    m_revision = revision;
}

Integer NodeAttributes::getName() const
{
    return m_name;
}

void NodeAttributes::setName(const Integer &name)
{
    m_name = name;
}

Integer NodeAttributes::getDescription() const
{
    return m_description;
}

void NodeAttributes::setDescription(const Integer &description)
{
    m_description = description;
}

Integer NodeAttributes::getReferences() const
{
    return m_references;
}

void NodeAttributes::setReferences(const Integer &references)
{
    m_references = references;
}

Integer NodeAttributes::getAttachments() const
{
    return m_attachments;
}

void NodeAttributes::setAttachments(const Integer &attachments)
{
    m_attachments = attachments;
}

Integer NodeAttributes::getComments() const
{
    return m_comments;
}

void NodeAttributes::setComments(const Integer &comments)
{
    m_comments = comments;
}

Boolean NodeAttributes::getIsActive() const
{
    return m_isActive;
}

void NodeAttributes::setIsActive(const Boolean &isActive)
{
    m_isActive = isActive;
}

NodeAttributes NodeAttributes::fromRecord(const QSqlRecord &record, bool *ok)
{
    NodeAttributes nodeAttributes;
    bool success = !record.isEmpty();

    // Id
    if (success)
    {
        nodeAttributes.setId(Integer::fromField(record.field("Id"), &success));
    }

    // Node
    if (success)
    {
        nodeAttributes.setNode(Integer::fromField(record.field("Node"), &success));
    }

    // Revision
    if (success)
    {
        nodeAttributes.setRevision(Integer::fromField(record.field("Revision"), &success));
    }

    // Name
    if (success)
    {
        nodeAttributes.setName(Integer::fromField(record.field("Name"), &success));
    }

    // Description
    if (success)
    {
        nodeAttributes.setDescription(Integer::fromField(record.field("Description"), &success));
    }

    // References
    if (success)
    {
        nodeAttributes.setReferences(Integer::fromField(record.field("References"), &success));
    }

    // Attachments
    if (success)
    {
        nodeAttributes.setAttachments(Integer::fromField(record.field("Attachments"), &success));
    }

    // Comments
    if (success)
    {
        nodeAttributes.setComments(Integer::fromField(record.field("Comments"), &success));
    }

    // IsActive
    if (success)
    {
        nodeAttributes.setIsActive(Boolean::fromField(record.field("IsActive"), &success));
    }

    // Check NodeAttributes
    if (!success ||
        !nodeAttributes.isValid())
    {
        nodeAttributes = NodeAttributes();
        success = false;
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return nodeAttributes;
}
