/**
 * @file   RevisionRecord.cpp
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-06-04
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

#include "Database/RevisionRecord.h"
#include <QtCore/QString>

using namespace Database;

RevisionRecord::RevisionRecord()
    : m_id(),
      m_timestamp(),
      m_user()
{
}

RevisionRecord::RevisionRecord(const IntegerField &id,
                               const DateTimeField &timestamp,
                               const IntegerField &user)
    : m_id(id),
      m_timestamp(timestamp),
      m_user(user)
{
}

bool RevisionRecord::isValid() const
{
    return (!m_id.isNull() &&
            !m_timestamp.isNull() &&
            !m_user.isNull());
}

IntegerField RevisionRecord::getId() const
{
    return m_id;
}

void RevisionRecord::setId(const IntegerField &id)
{
    m_id = id;
}

DateTimeField RevisionRecord::getTimestamp() const
{
    return m_timestamp;
}

void RevisionRecord::setTimestamp(const DateTimeField &timestamp)
{
    m_timestamp = timestamp;
}

IntegerField RevisionRecord::getUser() const
{
    return m_user;
}

void RevisionRecord::setUser(const IntegerField &user)
{
    m_user = user;
}

QDebug operator<<(QDebug dbg, const RevisionRecord &revision)
{
    dbg.nospace() << "< RevisionRecord: Id=" << revision.getId();
    dbg.nospace() << "Timestamp="<< revision.getTimestamp();
    dbg.nospace() << "User=" << revision.getUser() << ">";

    return dbg.space();
}
