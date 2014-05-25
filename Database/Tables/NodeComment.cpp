/**
 * @file   NodeComment.cpp
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

#include "Database/Tables/NodeComment.h"

using namespace Database::Tables;
using namespace Database::DataTypes;

NodeComment::NodeComment()
    : m_id(),
      m_text()
{
}

NodeComment::NodeComment(const Integer &id,
                         const Text &text)
    : m_id(id),
      m_text(text)
{
}

bool NodeComment::isValid() const
{
    return (!m_id.isNull() &&
            !m_text.isNull());
}

Integer NodeComment::getId() const
{
    return m_id;
}

void NodeComment::setId(const Integer &id)
{
    m_id = id;
}

Text NodeComment::getText() const
{
    return m_text;
}

void NodeComment::setText(const Text &text)
{
    m_text = text;
}

NodeComment NodeComment::fromRecord(const QSqlRecord &record, bool *ok)
{
    NodeComment nodeComment;
    bool success = !record.isEmpty();

    // Id
    if (success)
    {
        nodeComment.setId(Integer::fromField(record.field("Id"), &success));
    }

    // Text
    if (success)
    {
        nodeComment.setText(Text::fromField(record.field("Text"), &success));
    }

    // Check NodeComment
    if (!success ||
        !nodeComment.isValid())
    {
        nodeComment = NodeComment();
        success = false;
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return nodeComment;
}
