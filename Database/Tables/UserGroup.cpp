/**
 * @file   UserGroup.cpp
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

#include "Database/Tables/UserGroup.h"

using namespace Database::Tables;
using namespace Database::DataTypes;

UserGroup::UserGroup()
    : m_id(),
      m_name(),
      m_type(),
      m_description()
{
}

UserGroup::UserGroup(const Integer &id,
                     const Text &name,
                     const Integer &type,
                     const Text &description)
    : m_id(id),
      m_name(name),
      m_type(type),
      m_description(description)
{
}

bool UserGroup::isValid() const
{
    return (!m_id.isNull() &&
            !m_name.isNull() &&
            !m_type.isNull());
}

Integer UserGroup::getId() const
{
    return m_id;
}

void UserGroup::setId(const Integer &id)
{
    m_id = id;
}

Text UserGroup::getName() const
{
    return m_name;
}

void UserGroup::setName(const Text &name)
{
    m_name = name;
}

Integer UserGroup::getType() const
{
    return m_type;
}

void UserGroup::setType(const Integer &type)
{
    m_type = type;
}

Text UserGroup::getDescription() const
{
    return m_description;
}

void UserGroup::setDescription(const Text &description)
{
    m_description = description;
}

UserGroup UserGroup::fromRecord(const QSqlRecord &record, bool *ok)
{
    UserGroup userGroup;
    bool success = !record.isEmpty();

    // Id
    if (success)
    {
        userGroup.setId(Integer::fromField(record.field("Id"), &success));
    }

    // Name
    if (success)
    {
        userGroup.setName(Text::fromField(record.field("Name"), &success));
    }

    // Type
    if (success)
    {
        userGroup.setType(Integer::fromField(record.field("Type"), &success));
    }

    // Description
    if (success)
    {
        userGroup.setDescription(Text::fromField(record.field("Description"), &success));
    }

    // Check UserGroup
    if (!success ||
        !userGroup.isValid())
    {
        userGroup = UserGroup();
        success = false;
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return userGroup;
}
