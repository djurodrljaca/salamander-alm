/**
 * @file   User.cpp
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

#include "Database/Tables/User.h"

using namespace Database::Tables;
using namespace Database::DataTypes;

User::User()
    : m_id(),
      m_group(),
      m_name(),
      m_description(),
      m_password()
{
}

User::User(const Integer &id,
           const Integer &group,
           const Text &name,
           const Text &description,
           const Text &password)
    : m_id(id),
      m_group(group),
      m_name(name),
      m_description(description),
      m_password(password)
{
}

bool User::isValid() const
{
    return (!m_id.isNull() &&
            !m_group.isNull() &&
            !m_name.isNull() &&
            !m_password.isNull());
}

Integer User::getId() const
{
    return m_id;
}

void User::setId(const Integer &id)
{
    m_id = id;
}

Integer User::getGroup() const
{
    return m_group;
}

void User::setGroup(const Integer &group)
{
    m_group = group;
}

Text User::getName() const
{
    return m_name;
}

void User::setName(const Text &name)
{
    m_name = name;
}

Text User::getDescription() const
{
    return m_description;
}

void User::setDescription(const Text &description)
{
    m_description = description;
}

Text User::getPassword() const
{
    return m_password;
}

void User::setPassword(const Text &password)
{
    m_password = password;
}

User User::fromRecord(const QSqlRecord &record, bool *ok)
{
    User user;
    bool success = !record.isEmpty();

    // Id
    if (success)
    {
        user.setId(Integer::fromField(record.field("Id"), &success));
    }

    // Group
    if (success)
    {
        user.setGroup(Integer::fromField(record.field("Group"), &success));
    }

    // Name
    if (success)
    {
        user.setName(Text::fromField(record.field("Name"), &success));
    }

    // Description
    if (success)
    {
        user.setDescription(Text::fromField(record.field("Description"), &success));
    }

    // Password
    if (success)
    {
        user.setPassword(Text::fromField(record.field("Password"), &success));
    }

    // Check User
    if (!success ||
        !user.isValid())
    {
        user = User();
        success = false;
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return user;
}
