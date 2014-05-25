/**
 * @file   Blob.cpp
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

#include "Database/DataTypes/Blob.h"

using namespace Database::DataTypes;

Blob::Blob()
    : m_null(true),
      m_value()
{
}

Blob::Blob(const QByteArray &value)
    : m_null(false),
      m_value(value)
{
}

bool Blob::isNull() const
{
    return m_null;
}

void Blob::setNull()
{
    m_null = true;
    m_value = QByteArray();
}

QByteArray Blob::getValue() const
{
    return m_value;
}

void Blob::setValue(const QByteArray &value)
{
    m_null = false;
    m_value = value;
}

QVariant Blob::toVariant() const
{
    QVariant value(QVariant::ByteArray);

    if (!isNull())
    {
        value.setValue(m_value);
    }

    return value;
}

Blob Blob::fromField(const QSqlField &field, bool *ok)
{
    Blob blob;
    bool success = false;

    if (field.isValid())
    {
        if (field.isNull())
        {
            blob.setNull();
            success = true;
        }
        else
        {
            if (field.value().type() == QVariant::ByteArray)
            {
                blob.setValue(field.value().toByteArray());
                success = true;
            }
        }
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return blob;
}
