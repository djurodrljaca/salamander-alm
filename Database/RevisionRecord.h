/**
 * @file   RevisionRecord.h
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-06-04
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

#ifndef DATABASE_REVISIONRECORD_H
#define DATABASE_REVISIONRECORD_H

#include "Database/IntegerField.h"
#include "Database/DateTimeField.h"
#include <QtCore/QtDebug>

namespace Database
{
class RevisionRecord
{
public:
    RevisionRecord();
    RevisionRecord(const IntegerField &id,
                   const DateTimeField &timestamp,
                   const IntegerField &user);

    bool isValid() const;

    IntegerField getId() const;
    void setId(const IntegerField &id);

    DateTimeField getTimestamp() const;
    void setTimestamp(const DateTimeField &timestamp);

    IntegerField getUser() const;
    void setUser(const IntegerField &user);

private:
    IntegerField m_id;
    DateTimeField m_timestamp;
    IntegerField m_user;
};
}

QDebug operator<<(QDebug dbg, const Database::RevisionRecord &revision);

#endif // DATABASE_REVISIONRECORD_H
