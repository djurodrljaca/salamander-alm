/**
 * @file   UserRecord.h
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-06-03
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

#ifndef DATABASE_USERRECORD_H
#define DATABASE_USERRECORD_H

#include "Database/TextField.h"
#include "Database/UserType.h"

namespace Database
{
class UserRecord
{
public:
    UserRecord();
    UserRecord(const IntegerField &id,
               const UserType type,
               const TextField &fullName,
               const TextField &username,
               const TextField &password);

    bool isValid() const;

    IntegerField getId() const;
    void setId(const IntegerField &id);

    UserType getType() const;
    void setType(const UserType type);

    TextField getFullName() const;
    void setFullName(const TextField &fullName);

    TextField getUsername() const;
    void setUsername(const TextField &username);

    TextField getPassword() const;
    void setPassword(const TextField &password);

private:
    IntegerField m_id;
    UserType m_type;
    TextField m_fullName;
    TextField m_username;
    TextField m_password;
};
}

QDebug operator<<(QDebug dbg, const Database::UserRecord &user);

#endif // DATABASE_USERRECORD_H
