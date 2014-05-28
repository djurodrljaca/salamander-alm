/**
 * @file   IntegerField.cpp
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

#include "Database/IntegerField.h"
#include <QtCore/QString>

using namespace Database;

IntegerField::IntegerField()
    : m_null(true),
      m_value(0LL)
{
}

IntegerField::IntegerField(const qlonglong value)
    : m_null(false),
      m_value(value)
{
}

bool IntegerField::operator ==(const IntegerField &other) const
{
    bool equal = false;

    if (m_null && other.m_null)
    {
        equal = true;
    }
    else if (!m_null && !other.m_null)
    {
        if (m_value == other.m_value)
        {
            equal = true;
        }
    }

    return equal;
}

bool IntegerField::operator !=(const IntegerField &other) const
{
    return !operator ==(other);
}

bool IntegerField::isNull() const
{
    return m_null;
}

void IntegerField::setNull()
{
    m_null = true;
    m_value = 0LL;
}

qlonglong IntegerField::getValue() const
{
    return m_value;
}

void IntegerField::setValue(const qlonglong value)
{
    m_null = false;
    m_value = value;
}

QDebug operator<<(QDebug dbg, const IntegerField &integer)
{
    if (integer.isNull())
    {
        dbg.nospace() << "NULL";
    }
    else
    {
        dbg.nospace() << integer.getValue();
    }

    return dbg.space();
}
