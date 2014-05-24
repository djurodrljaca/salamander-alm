/**
 * @file   NodeType.cpp
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-5-24
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

#include "NodeType.h"

using namespace Database;

NodeType::NodeType()
    : m_id(),
      m_name()
{
}

NodeType::NodeType(const Id id, QString name)
    : m_id(id),
      m_name(name)
{
}

bool NodeType::isValid() const
{
    bool valid = false;

    if (!m_id.isNull())
    {
        switch (m_id.getValue())
        {
            case NodeType::Project:
            {
                valid = true;
                break;
            }

            default:
            {
                valid = false;
                break;
            }
        }
    }

    return valid;
}

Id NodeType::getId() const
{
    return m_id;
}

void NodeType::setId(const Id id)
{
    m_id = id;
}

QString NodeType::getName() const
{
    return m_name;
}

void NodeType::setName(const QString &name)
{
    m_name = name;
}

NodeType NodeType::fromRecord(const QSqlRecord &record, bool *ok)
{
    NodeType nodeType;
    bool success = !record.isEmpty();

    // Id
    if (success)
    {
        nodeType.setId(Id::fromField(record.field("Id"), &success));
    }

    // Name
    if (success)
    {
        // TODO: implement
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return nodeType;
}
