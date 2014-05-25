/**
 * @file   Integer.cpp
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

#include "Database/DataTypes/Integer.h"

using namespace Database::DataTypes;

Integer::Integer()
    : m_null(true),
      m_value(-1LL)
{
}

Integer::Integer(const qint64 value)
    : m_null(false),
      m_value(value)
{
}

bool Integer::isNull() const
{
    return m_null;
}

void Integer::setNull()
{
    m_null = true;
    m_value = -1LL;
}

qint64 Integer::getValue() const
{
    return m_value;
}

void Integer::setValue(const qint64 value)
{
    m_null = false;
    m_value = value;
}

Integer Integer::fromField(const QSqlField &field, bool *ok)
{
    Integer integer;
    bool success = false;

    if (field.isValid())
    {
        if (field.isNull())
        {
            integer.setNull();
            success = true;
        }
        else
        {
            const qint64 value = field.value().toLongLong(&success);

            if (success)
            {
                integer.setValue(value);
            }
        }
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return integer;
}