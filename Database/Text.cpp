/**
 * @file   Text.cpp
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

#include "Database/Text.h"

using namespace Database;

Text::Text()
    : m_null(true),
      m_value()
{
}

Text::Text(const QString &value)
    : m_null(false),
      m_value(value)
{
}

bool Text::isNull() const
{
    return m_null;
}

void Text::setNull()
{
    m_null = true;
    m_value = QString();
}

QString Text::getValue() const
{
    return m_value;
}

void Text::setValue(const QString &value)
{
    m_null = false;
    m_value = value;
}
