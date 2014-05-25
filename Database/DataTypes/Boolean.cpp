/**
 * @file   Boolean.cpp
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

#include "Database/DataTypes/Boolean.h"

using namespace Database::DataTypes;

Boolean::Boolean()
    : m_null(true),
      m_value(false)
{
}

Boolean::Boolean(const bool value)
    : m_null(false),
      m_value(value)
{
}

bool Boolean::isNull() const
{
    return m_null;
}

void Boolean::setNull()
{
    m_null = true;
    m_value = false;
}

bool Boolean::getValue() const
{
    return m_value;
}

void Boolean::setValue(const bool value)
{
    m_null = false;
    m_value = value;
}

QVariant Boolean::toVariant() const
{
    QVariant value(QVariant::Bool);

    if (!isNull())
    {
        value.setValue(m_value);
    }

    return value;
}

Boolean Boolean::fromField(const QSqlField &field, bool *ok)
{
    Boolean boolean;
    bool success = false;

    if (field.isValid())
    {
        if (field.isNull())
        {
            boolean.setNull();
            success = true;
        }
        else
        {
            const qint64 value = field.value().toLongLong(&success);

            if (success)
            {
                switch (value)
                {
                    case 0:
                    {
                        boolean.setValue(false);
                        break;
                    }

                    case 1:
                    {
                        boolean.setValue(true);
                        break;
                    }

                    default:
                    {
                        success = false;
                        break;
                    }
                }
            }
        }
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return boolean;
}
