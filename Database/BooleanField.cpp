/**
 * @file   BooleanField.cpp
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

#include "Database/BooleanField.h"

using namespace Database;

BooleanField::BooleanField()
    : m_null(true),
      m_value(false)
{
}

BooleanField::BooleanField(const bool value)
    : m_null(false),
      m_value(value)
{
}

bool BooleanField::operator ==(const BooleanField &other) const
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

bool BooleanField::operator !=(const BooleanField &other) const
{
    return !operator ==(other);
}

bool BooleanField::isNull() const
{
    return m_null;
}

void BooleanField::setNull()
{
    m_null = true;
    m_value = false;
}

bool BooleanField::getValue() const
{
    return m_value;
}

void BooleanField::setValue(const bool value)
{
    m_null = false;
    m_value = value;
}
