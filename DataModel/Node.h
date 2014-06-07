/**
 * @file   NodeRecord.h
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-05-27
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

#ifndef DATAMODEL_NODE_H
#define DATAMODEL_NODE_H

#include "Database/IntegerField.h"
#include "Database/NodeType.h"
#include <QtCore/QList>

namespace DataModel
{
class Node
{
public:
    Node();

    bool isValid() const;

    Database::IntegerField getId() const;
    void setId(const Database::IntegerField &id);

    Database::NodeType getType() const;
    void setType(const Database::NodeType type);

    QString getName() const;
    void setName(const QString &name);

    QString getDescription() const;
    void setDescription(const QString &description);

private:
    Database::IntegerField m_id;
    Database::NodeType m_type;
    QString m_name;
    QString m_description;
};
}

#endif // DATAMODEL_NODE_H
