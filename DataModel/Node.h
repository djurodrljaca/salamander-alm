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
    Node(const Database::IntegerField &id,
         const Database::NodeType type,
         const QString &name = QString(),
         const QString &description = QString(),
         const bool active = true);

    void clear();
    bool isValid() const;
    bool hasChanged() const;
    void acceptChanges();

    Database::IntegerField getId() const;

    Database::NodeType getType() const;

    QString getName() const;
    void setName(const QString &name);
    bool nameChanged() const;

    QString getDescription() const;
    void setDescription(const QString &description);
    bool descriptionChanged() const;

    bool getActive() const;
    void setActive(const bool active);
    bool activeChanged() const;

private:
    Database::IntegerField m_id;
    Database::NodeType m_type;
    QString m_name;
    bool m_nameChanged;
    QString m_description;
    bool m_descriptionChanged;
    bool m_active;
    bool m_activeChanged;
};
}

#endif // DATAMODEL_NODE_H
