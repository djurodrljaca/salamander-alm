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

#include "Database/Tables/NodeType.h"

using namespace Database::Tables;
using namespace Database::DataTypes;

NodeType::NodeType()
    : m_id(),
      m_name()
{
}

NodeType::NodeType(const Integer &id,
                   const Text &name)
    : m_id(id),
      m_name(name)
{
}

bool NodeType::isValid() const
{
    bool valid = false;

    if (!m_id.isNull() &&
        !m_name.isNull())
    {
        switch (m_id.getValue())
        {
            case NodeType::Project:
            {
                if (m_name.getValue() == "Project")
                {
                    valid = true;
                }
                break;
            }

            default:
            {
                break;
            }
        }
    }

    return valid;
}

Integer NodeType::getId() const
{
    return m_id;
}

void NodeType::setId(const Integer &id)
{
    m_id = id;
}

Text NodeType::getName() const
{
    return m_name;
}

void NodeType::setName(const Text &name)
{
    m_name = name;
}

QString NodeType::toString() const
{
    static const QString str("NodeType (Id='%1' Name='%2')");

    return str.arg(m_id.toString(),
                   m_name.toString());
}
