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

#include "DatabaseId.h"

DatabaseId::DatabaseId()
    : m_null(true),
      m_id(-1LL)
{
}

DatabaseId::DatabaseId(const qint64 id)
    : m_null(false),
      m_id(id)
{
}

bool DatabaseId::isNull()
{
    return m_null;
}

void DatabaseId::setNull()
{
    m_null = true;
    m_id = -1LL;
}

qint64 DatabaseId::getId()
{
    return m_id;
}

void DatabaseId::setId(const qint64 id)
{
    m_null = false;
    m_id = id;
}
