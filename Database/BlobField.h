/**
 * @file   BlobField.h
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

#ifndef DATABASE_BLOBFIELD_H
#define DATABASE_BLOBFIELD_H

#include <QtCore/QByteArray>

namespace Database
{
class BlobField
{
public:
    BlobField();
    BlobField(const QByteArray &value);

    bool operator ==(const BlobField& other) const;
    bool operator !=(const BlobField& other) const;

    bool isNull() const;
    void setNull();
    QByteArray getValue() const;
    void setValue(const QByteArray &value);

private:
    bool m_null;
    QByteArray m_value;
};
}

#endif // DATABASE_BLOBFIELD_H
