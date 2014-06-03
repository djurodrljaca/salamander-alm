/**
 * @file   UserRecord.cpp
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-05-24
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

#include "Database/UserRecord.h"

using namespace Database;

UserRecord::UserRecord()
    : m_id(),
      m_type(UserType_Invalid),
      m_fullName(),
      m_username(),
      m_password()
{
}

UserRecord::UserRecord(const IntegerField &id,
                       const UserType type,
                       const TextField &fullName,
                       const TextField &username,
                       const TextField &password)
    : m_id(id),
      m_type(type),
      m_fullName(fullName),
      m_username(username),
      m_password(password)
{
}

bool UserRecord::isValid() const
{
    return (isUserTypeValid(m_type) &&
            !m_fullName.isNull() &&
            !m_username.isNull() &&
            !m_password.isNull());
}

IntegerField UserRecord::getId() const
{
    return m_id;
}

void UserRecord::setId(const IntegerField &id)
{
    m_id = id;
}

UserType UserRecord::getType() const
{
    return m_type;
}

void UserRecord::setType(const UserType type)
{
    m_type = type;
}

TextField UserRecord::getFullName() const
{
    return m_fullName;
}

void UserRecord::setFullName(const TextField &fullName)
{
    m_fullName = fullName;
}

TextField UserRecord::getUsername() const
{
    return m_username;
}

void UserRecord::setUsername(const TextField &username)
{
    m_username = username;
}

TextField UserRecord::getPassword() const
{
    return m_password;
}

void UserRecord::setPassword(const TextField &password)
{
    m_password = password;
}

QDebug operator<<(QDebug dbg, const UserRecord &node)
{
    dbg.nospace() << "< UserRecord: Id=" << node.getId();
    dbg.nospace() << "Type="<< node.getType();
    dbg.nospace() << "FullName="<< node.getFullName();
    dbg.nospace() << "Username="<< node.getUsername();
    dbg.nospace() << "Password=" << node.getPassword() << ">";

    return dbg.space();
}
