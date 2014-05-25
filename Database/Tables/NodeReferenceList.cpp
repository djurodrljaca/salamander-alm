/**
 * @file   NodeReferenceList.cpp
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-5-25
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

#include "Database/Tables/NodeReferenceList.h"

using namespace Database::Tables;
using namespace Database::DataTypes;

NodeReferenceList::NodeReferenceList()
    : m_id()
{
}

NodeReferenceList::NodeReferenceList(const Integer &id)
    : m_id(id)
{
}

bool NodeReferenceList::isValid() const
{
    return !m_id.isNull();
}

Integer NodeReferenceList::getId() const
{
    return m_id;
}

void NodeReferenceList::setId(const Integer &id)
{
    m_id = id;
}

NodeReferenceList NodeReferenceList::fromRecord(const QSqlRecord &record, bool *ok)
{
    NodeReferenceList nodeReferenceList;
    bool success = !record.isEmpty();

    // Id
    if (success)
    {
        nodeReferenceList.setId(Integer::fromField(record.field("Id"), &success));
    }

    // Check NodeReferenceList
    if (!success ||
        !nodeReferenceList.isValid())
    {
        nodeReferenceList = NodeReferenceList();
        success = false;
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return nodeReferenceList;
}
