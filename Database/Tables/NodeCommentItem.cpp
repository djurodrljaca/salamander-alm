/**
 * @file   NodeCommentItem.cpp
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

#include "Database/Tables/NodeCommentItem.h"

using namespace Database::Tables;
using namespace Database::DataTypes;

NodeCommentItem::NodeCommentItem()
    : m_id(),
      m_list(),
      m_comment()
{
}

NodeCommentItem::NodeCommentItem(const Integer &id,
                                 const Integer &list,
                                 const Integer &comment)
    : m_id(id),
      m_list(list),
      m_comment(comment)
{
}

bool NodeCommentItem::isValid() const
{
    return (!m_id.isNull() &&
            !m_list.isNull() &&
            !m_comment.isNull());
}

Integer NodeCommentItem::getId() const
{
    return m_id;
}

void NodeCommentItem::setId(const Integer &id)
{
    m_id = id;
}

Integer NodeCommentItem::getList() const
{
    return m_list;
}

void NodeCommentItem::setList(const Integer &list)
{
    m_list = list;
}

Integer NodeCommentItem::getComment() const
{
    return m_comment;
}

void NodeCommentItem::setComment(const Integer &comment)
{
    m_comment = comment;
}

NodeCommentItem NodeCommentItem::fromRecord(const QSqlRecord &record, bool *ok)
{
    NodeCommentItem node;
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

    // Comment
    if (success)
    {
        node.setComment(Integer::fromField(record.field("Comment"), &success));
    }

    // Check NodeCommentItem
    if (!success ||
        !node.isValid())
    {
        node = NodeCommentItem();
        success = false;
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return node;
}
