/**
 * @file   Node.h
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

#include "Database/Integer.h"
#include "Database/NodeType.h"
#include <QtCore/QList>

namespace DataModel
{
class Node
{
public:
    Node();
    Node(const Node &other);
    ~Node();

    Node & operator=(const Node &other);

    bool isValid() const;

    Database::Integer getId() const;
    void setId(const Database::Integer &id);

    Database::NodeType getType() const;
    void setType(const Database::NodeType type);

    Node * getParent() const;
    void setParent(const Node *parent);

    int getChildrenCount() const;
    bool addChild(const Node &child);
    Node * getChild(const int index);

private:
    Database::Integer m_id;
    Database::NodeType m_type;
    Node *m_parent;
    QList<Node> m_children;
};
}

#endif // DATAMODEL_NODE_H
