/**
 * @file   NodeNameRecord.cpp
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-06-05
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

#include "Database/NodeNameRecord.h"

using namespace Database;

NodeNameRecord::NodeNameRecord()
    : m_id(),
      m_text()
{
}

NodeNameRecord::NodeNameRecord(const IntegerField &id,
                               const TextField &text)
    : m_id(id),
      m_text(text)
{
}

bool NodeNameRecord::isValid() const
{
    return !m_text.isNull();
}

IntegerField NodeNameRecord::getId() const
{
    return m_id;
}

void NodeNameRecord::setId(const IntegerField &id)
{
    m_id = id;
}

TextField NodeNameRecord::getText() const
{
    return m_text;
}

void NodeNameRecord::setText(const TextField &text)
{
    m_text = text;
}

QDebug operator<<(QDebug dbg, const NodeNameRecord &nodeName)
{
    dbg.nospace() << "< NodeNameRecord: Id=" << nodeName.getId();
    dbg.nospace() << "Text=" << nodeName.getText() << ">";

    return dbg.space();
}
