/**
 * @file   NodeReferenceItem.cpp
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

#include "Database/Tables/NodeReferenceItem.h"

using namespace Database::Tables;
using namespace Database::DataTypes;

NodeReferenceItem::NodeReferenceItem()
    : m_id(),
      m_list(),
      m_reference()
{
}

NodeReferenceItem::NodeReferenceItem(const Integer &id,
                                     const Integer &list,
                                     const Integer &reference)
    : m_id(id),
      m_list(list),
      m_reference(reference)
{
}

bool NodeReferenceItem::isValid() const
{
    return (!m_id.isNull() &&
            !m_list.isNull() &&
            !m_reference.isNull());
}

Integer NodeReferenceItem::getId() const
{
    return m_id;
}

void NodeReferenceItem::setId(const Integer &id)
{
    m_id = id;
}

Integer NodeReferenceItem::getList() const
{
    return m_list;
}

void NodeReferenceItem::setList(const Integer &list)
{
    m_list = list;
}

Integer NodeReferenceItem::getReference() const
{
    return m_reference;
}

void NodeReferenceItem::setReference(const Integer &reference)
{
    m_reference = reference;
}

NodeReferenceItem NodeReferenceItem::fromRecord(const QSqlRecord &record, bool *ok)
{
    NodeReferenceItem node;
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

    // Reference
    if (success)
    {
        node.setReference(Integer::fromField(record.field("Reference"), &success));
    }

    // Check NodeReferenceItem
    if (!success ||
        !node.isValid())
    {
        node = NodeReferenceItem();
        success = false;
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return node;
}
