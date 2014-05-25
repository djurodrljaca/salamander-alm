/**
 * @file   Revision.cpp
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

#include "Database/Tables/Revision.h"

using namespace Database::Tables;
using namespace Database::DataTypes;

Revision::Revision()
    : m_id(),
      m_timestamp(),
      m_user()
{
}

Revision::Revision(const Integer &id,
                   const DateTime &timestamp,
                   const Integer &user)
    : m_id(id),
      m_timestamp(timestamp),
      m_user(user)
{
}

bool Revision::isValid() const
{
    return (!m_id.isNull() &&
            !m_timestamp.isNull() &&
            !m_user.isNull());
}

Integer Revision::getId() const
{
    return m_id;
}

void Revision::setId(const Integer &id)
{
    m_id = id;
}

DateTime Revision::getTimestamp() const
{
    return m_timestamp;
}

void Revision::setTimestamp(const DateTime &timestamp)
{
    m_timestamp = timestamp;
}

Integer Revision::getUser() const
{
    return m_user;
}

void Revision::setUser(const Integer &user)
{
    m_user = user;
}

Revision Revision::fromRecord(const QSqlRecord &record, bool *ok)
{
    Revision revision;
    bool success = !record.isEmpty();

    // Id
    if (success)
    {
        revision.setId(Integer::fromField(record.field("Id"), &success));
    }

    // Timestamp
    if (success)
    {
        revision.setTimestamp(DateTime::fromField(record.field("Timestamp"), &success));
    }

    // User
    if (success)
    {
        revision.setUser(Integer::fromField(record.field("User"), &success));
    }

    // Check Revision
    if (!success ||
        !revision.isValid())
    {
        revision = Revision();
        success = false;
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return revision;
}
