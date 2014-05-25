/**
 * @file   NodeAttachmentList.cpp
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

#include "Database/Tables/NodeAttachmentList.h"

using namespace Database::Tables;
using namespace Database::DataTypes;

NodeAttachmentList::NodeAttachmentList()
    : m_id()
{
}

NodeAttachmentList::NodeAttachmentList(const Integer &id)
    : m_id(id)
{
}

bool NodeAttachmentList::isValid() const
{
    return !m_id.isNull();
}

Integer NodeAttachmentList::getId() const
{
    return m_id;
}

void NodeAttachmentList::setId(const Integer &id)
{
    m_id = id;
}

NodeAttachmentList NodeAttachmentList::fromRecord(const QSqlRecord &record, bool *ok)
{
    NodeAttachmentList nodeAttachmentList;
    bool success = !record.isEmpty();

    // Id
    if (success)
    {
        nodeAttachmentList.setId(Integer::fromField(record.field("Id"), &success));
    }

    // Check NodeAttachmentList
    if (!success ||
        !nodeAttachmentList.isValid())
    {
        nodeAttachmentList = NodeAttachmentList();
        success = false;
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return nodeAttachmentList;
}
