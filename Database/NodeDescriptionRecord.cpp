/**
 * @file   NodeDescriptionRecord.cpp
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

#include "Database/NodeDescriptionRecord.h"

using namespace Database;

NodeDescriptionRecord::NodeDescriptionRecord()
    : m_id(),
      m_text()
{
}

NodeDescriptionRecord::NodeDescriptionRecord(const IntegerField &id,
                                             const TextField &text)
    : m_id(id),
      m_text(text)
{
}

bool NodeDescriptionRecord::isValid() const
{
    return !m_text.isNull();
}

IntegerField NodeDescriptionRecord::getId() const
{
    return m_id;
}

void NodeDescriptionRecord::setId(const IntegerField &id)
{
    m_id = id;
}

TextField NodeDescriptionRecord::getText() const
{
    return m_text;
}

void NodeDescriptionRecord::setText(const TextField &text)
{
    m_text = text;
}

QDebug operator<<(QDebug dbg, const NodeDescriptionRecord &nodeDescription)
{
    dbg.nospace() << "< NodeDescriptionRecord: Id=" << nodeDescription.getId();
    dbg.nospace() << "Text=" << nodeDescription.getText() << ">";

    return dbg.space();
}
