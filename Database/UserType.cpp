/**
 * @file   UserType.cpp
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

#include "Database/UserType.h"
#include <QtCore/QString>

bool Database::isUserTypeValid(const UserType userType)
{
    bool valid = false;

    switch (userType)
    {
        case UserType_Administrator:
        case UserType_User:
        {
            valid = true;
            break;
        }

        default:
        {
            break;
        }
    }

    return valid;
}

Database::IntegerField Database::convertUserTypeToInteger(const UserType userType, bool *ok)
{
    IntegerField integer;
    bool success = false;

    if (isUserTypeValid(userType))
    {
        integer.setValue(static_cast<qlonglong>(userType));
        success = true;
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return integer;
}

Database::UserType Database::convertIntegerToUserType(const IntegerField &integer, bool *ok)
{
    bool success = false;
    UserType userType = UserType_Invalid;

    if (!integer.isNull())
    {
        const UserType value = static_cast<UserType>(integer.getValue());

        if (isUserTypeValid(value))
        {
            userType = value;
            success = true;
        }
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return userType;
}

QDebug operator<<(QDebug dbg, const Database::UserType userType)
{
    switch (userType)
    {
        case Database::UserType_Administrator:
        {
            dbg.nospace() << "Administrator";
            break;
        }

        case Database::UserType_User:
        {
            dbg.nospace() << "User";
            break;
        }

        case Database::UserType_Invalid:
        default:
        {
            dbg.nospace() << "Invalid";
            break;
        }
    }

    return dbg.space();
}
