/**
 * @file   Boolean.h
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

#ifndef BOOL_H
#define BOOL_H

#include <QtGlobal>
#include <QtSql/QSqlField>

namespace Database
{
namespace DataTypes
{
class Boolean
{
public:
    Boolean();
    Boolean(const bool value);

    bool isNull() const;
    void setNull();
    bool getValue() const;
    void setValue(const bool value);

    static Boolean fromField(const QSqlField &field, bool *ok = NULL);

private:
    bool m_null;
    bool m_value;
};
}
}

#endif // BOOL_H
