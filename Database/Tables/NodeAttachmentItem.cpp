/**
 * @file   NodeAttachmentItem.cpp
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

#include "Database/Tables/NodeAttachmentItem.h"

using namespace Database::Tables;
using namespace Database::DataTypes;

NodeAttachmentItem::NodeAttachmentItem()
    : m_id(),
      m_list(),
      m_attachment()
{
}

NodeAttachmentItem::NodeAttachmentItem(const Integer &id,
                                       const Integer &list,
                                       const Integer &attachment)
    : m_id(id),
      m_list(list),
      m_attachment(attachment)
{
}

bool NodeAttachmentItem::isValid() const
{
    return (!m_id.isNull() &&
            !m_list.isNull() &&
            !m_attachment.isNull());
}

Integer NodeAttachmentItem::getId() const
{
    return m_id;
}

void NodeAttachmentItem::setId(const Integer &id)
{
    m_id = id;
}

Integer NodeAttachmentItem::getList() const
{
    return m_list;
}

void NodeAttachmentItem::setList(const Integer &list)
{
    m_list = list;
}

Integer NodeAttachmentItem::getAttachment() const
{
    return m_attachment;
}

void NodeAttachmentItem::setAttachment(const Integer &attachment)
{
    m_attachment = attachment;
}

NodeAttachmentItem NodeAttachmentItem::fromRecord(const QSqlRecord &record, bool *ok)
{
    NodeAttachmentItem node;
    bool success = !record.isEmpty();

    // Id
    if (success)
    {
        node.setId(Integer::fromField(record.field("Id"), &success));
    }

    // List
    if (success)
    {
        node.setList(Integer::fromField(record.field("List"), &success));
    }

    // Attachment
    if (success)
    {
        node.setAttachment(Integer::fromField(record.field("Attachment"), &success));
    }

    // Check NodeAttachmentItem
    if (!success ||
        !node.isValid())
    {
        node = NodeAttachmentItem();
        success = false;
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return node;
}
