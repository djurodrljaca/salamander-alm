/**
 * @file   TextField.h
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

#ifndef DATABASE_TEXT_H
#define DATABASE_TEXT_H

#include <QtCore/QString>
#include <QtCore/QDebug>

namespace Database
{
class TextField
{
public:
    TextField();
    TextField(const QString &value);

    bool operator ==(const TextField& other) const;
    bool operator !=(const TextField& other) const;

    bool isNull() const;
    void setNull();
    QString getValue() const;
    void setValue(const QString &value);

private:
    bool m_null;
    QString m_value;
};
}

QDebug operator<<(QDebug dbg, const Database::TextField &text);

#endif // DATABASE_TEXT_H