/**
 * @file   NodeType.h
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

#ifndef NODETYPE_H
#define NODETYPE_H

#include "Id.h"
#include <QtCore/QString>
#include <QtSql/QSqlRecord>

namespace Database
{
class NodeType
{
public:
    enum
    {
        Project = 1
    };

    NodeType();
    NodeType(const Id id, QString name);

    bool isValid() const;

    Id getId() const;
    void setId(const Id id);

    QString getName() const;
    void setName(const QString &name);

    static NodeType fromRecord(const QSqlRecord &record, bool *ok = NULL);

private:
    Id m_id;
    QString m_name;
};
}

#endif // NODETYPE_H
