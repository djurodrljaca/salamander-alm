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
    ~Node();

    bool isValid() const;

    Database::IntegerField getId() const;
    void setId(const Database::IntegerField &id);

    Node * getParent() const;
    void setParent(Node *parent);

    Database::NodeType getType() const;
    void setType(const Database::NodeType type);

    Database::IntegerField getRevisionId() const;
    void setRevisionId(const Database::IntegerField &revisionId);

    QString getName() const;
    void setName(const QString &name);

    Database::IntegerField getDescriptionId() const;
    void setDescriptionId(const Database::IntegerField &descriptionId);

    Database::IntegerField getReferencesId() const;
    void setReferencesId(const Database::IntegerField &referencesId);

    Database::IntegerField getAttachmentsId() const;
    void setAttachmentsId(const Database::IntegerField &attachmentsId);

    Database::IntegerField getCommentsId() const;
    void setCommentsId(const Database::IntegerField &commentsId);

    int getChildCount() const;
    Node * getChild(const int index) const;
    int getChildIndex(Node * const child) const;
    bool addChild(Node *child);

private:
    Database::IntegerField m_id;
    Node *m_parent;
    Database::NodeType m_type;
    Database::IntegerField m_revisionId;
    QString m_name;
    Database::IntegerField m_descriptionId;
    Database::IntegerField m_referencesId;
    Database::IntegerField m_attachmentsId;
    Database::IntegerField m_commentsId;
    QList<Node *> m_childList;
};
}

#endif // DATAMODEL_NODE_H
