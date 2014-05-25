/**
 * @file   NodeReference.cpp
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

#include "Database/Tables/NodeReference.h"

using namespace Database::Tables;
using namespace Database::DataTypes;

NodeReference::NodeReference()
    : m_id(),
      m_node()
{
}

NodeReference::NodeReference(const Integer &id,
                             const Integer &node)
    : m_id(id),
      m_node(node)
{
}

bool NodeReference::isValid() const
{
    return (!m_id.isNull() &&
            !m_node.isNull());
}

Integer NodeReference::getId() const
{
    return m_id;
}

void NodeReference::setId(const Integer &id)
{
    m_id = id;
}

Integer NodeReference::getNode() const
{
    return m_node;
}

void NodeReference::setNode(const Integer &node)
{
    m_node = node;
}

NodeReference NodeReference::fromRecord(const QSqlRecord &record, bool *ok)
{
    NodeReference nodeReference;
    bool success = !record.isEmpty();

    // Id
    if (success)
    {
        nodeReference.setId(Integer::fromField(record.field("Id"), &success));
    }

    // Node
    if (success)
    {
        nodeReference.setNode(Integer::fromField(record.field("Node"), &success));
    }

    // Check NodeReference
    if (!success ||
        !nodeReference.isValid())
    {
        nodeReference = NodeReference();
        success = false;
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return nodeReference;
}
