/**
 * @file   DatabaseId.cpp
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-5-24
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

#include "Id.h"

using namespace Database;

Id::Id()
    : m_null(true),
      m_value(-1LL)
{
}

Id::Id(const qint64 value)
    : m_null(false),
      m_value(value)
{
}

bool Id::isNull() const
{
    return m_null;
}

void Id::setNull()
{
    m_null = true;
    m_value = -1LL;
}

qint64 Id::getValue() const
{
    return m_value;
}

void Id::setValue(const qint64 value)
{
    m_null = false;
    m_value = value;
}

Id Id::fromField(const QSqlField &field, bool *ok)
{
    Id id;
    bool success = false;

    if (field.isValid() && (field.name() == "Id"))
    {
        if (field.isNull())
        {
            id.setNull();
            success = true;
        }
        else
        {
            const qint64 value = field.value().toLongLong(&success);

            if (success)
            {
                id.setValue(value);
            }
        }
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return id;
}
