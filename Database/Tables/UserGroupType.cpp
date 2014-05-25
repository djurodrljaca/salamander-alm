/**
 * @file   UserGroupType.cpp
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

#include "Database/Tables/UserGroupType.h"

using namespace Database::Tables;
using namespace Database::DataTypes;

UserGroupType::UserGroupType()
    : m_id(),
      m_name()
{
}

UserGroupType::UserGroupType(const Integer &id,
                             const Text &name)
    : m_id(id),
      m_name(name)
{
}

bool UserGroupType::isValid() const
{
    bool valid = false;

    if (!m_id.isNull() &&
        !m_name.isNull())
    {
        switch (m_id.getValue())
        {
            case UserGroupType::Administrator:
            {
                if (m_name.getValue() == "Administrator")
                {
                    valid = true;
                }
                break;
            }

            case UserGroupType::User:
            {
                if (m_name.getValue() == "User")
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

Integer UserGroupType::getId() const
{
    return m_id;
}

void UserGroupType::setId(const Integer &id)
{
    m_id = id;
}

Text UserGroupType::getName() const
{
    return m_name;
}

void UserGroupType::setName(const Text &name)
{
    m_name = name;
}

UserGroupType UserGroupType::fromRecord(const QSqlRecord &record, bool *ok)
{
    UserGroupType userGroupType;
    bool success = !record.isEmpty();

    // Id
    if (success)
    {
        userGroupType.setId(Integer::fromField(record.field("Id"), &success));
    }

    // Name
    if (success)
    {
        userGroupType.setName(Text::fromField(record.field("Name"), &success));
    }

    // Check UserGroupType
    if (!success ||
        !userGroupType.isValid())
    {
        userGroupType = UserGroupType();
        success = false;
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return userGroupType;
}
