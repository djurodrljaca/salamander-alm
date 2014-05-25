/**
 * @file   NodeDescription.cpp
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

#include "Database/Tables/NodeDescription.h"

using namespace Database::Tables;
using namespace Database::DataTypes;

NodeDescription::NodeDescription()
    : m_id(),
      m_text()
{
}

NodeDescription::NodeDescription(const Integer &id,
                                 const Text &text)
    : m_id(id),
      m_text(text)
{
}

bool NodeDescription::isValid() const
{
    return (!m_id.isNull() &&
            !m_text.isNull());
}

Integer NodeDescription::getId() const
{
    return m_id;
}

void NodeDescription::setId(const Integer &id)
{
    m_id = id;
}

Text NodeDescription::getText() const
{
    return m_text;
}

void NodeDescription::setText(const Text &text)
{
    m_text = text;
}

NodeDescription NodeDescription::fromRecord(const QSqlRecord &record, bool *ok)
{
    NodeDescription nodeName;
    bool success = !record.isEmpty();

    // Id
    if (success)
    {
        nodeName.setId(Integer::fromField(record.field("Id"), &success));
    }

    // Text
    if (success)
    {
        nodeName.setText(Text::fromField(record.field("Text"), &success));
    }

    // Check NodeDescription
    if (!success ||
        !nodeName.isValid())
    {
        nodeName = NodeDescription();
        success = false;
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return nodeName;
}
