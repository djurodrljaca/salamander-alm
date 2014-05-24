/**
 * @file   DatabaseId.h
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

#ifndef DATABASEID_H
#define DATABASEID_H

#include <QtGlobal>
#include <QtSql/QSqlField>

namespace Database
{
class Id
{
public:
    Id();
    Id(const qint64 value);

    bool isNull() const;
    void setNull();
    qint64 getValue() const;
    void setValue(const qint64 value);

    static Id fromField(const QSqlField &field, bool *ok = NULL);

private:
    bool m_null;
    qint64 m_value;
};
}

#endif // DATABASEID_H
