/**
 * @file   NodeAttributesRecord.h
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-06-05
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

#ifndef DATABASE_NODEATTRIBUTESRECORD_H
#define DATABASE_NODEATTRIBUTESRECORD_H

#include "Database/IntegerField.h"
#include "Database/BooleanField.h"
#include <QtCore/QtDebug>

namespace Database
{
class NodeAttributesRecord
{
public:
    NodeAttributesRecord();
    NodeAttributesRecord(const IntegerField &id,
                         const IntegerField &node,
                         const IntegerField &revision,
                         const IntegerField &name,
                         const IntegerField &description,
                         const IntegerField &references,
                         const IntegerField &attachments,
                         const IntegerField &comments,
                         const BooleanField &isActive);

    bool isValid() const;

    IntegerField getId() const;
    void setId(const IntegerField &id);

    IntegerField getNode() const;
    void setNode(const IntegerField &node);

    IntegerField getRevision() const;
    void setRevision(const IntegerField &revision);

    IntegerField getName() const;
    void setName(const IntegerField &name);

    IntegerField getDescription() const;
    void setDescription(const IntegerField &description);

    IntegerField getReferences() const;
    void setReferences(const IntegerField &references);

    IntegerField getAttachments() const;
    void setAttachments(const IntegerField &attachments);

    IntegerField getComments() const;
    void setComments(const IntegerField &comments);

    BooleanField getIsActive() const;
    void setIsActive(const BooleanField &isActive);

private:
    IntegerField m_id;
    IntegerField m_node;
    IntegerField m_revision;
    IntegerField m_name;
    IntegerField m_description;
    IntegerField m_references;
    IntegerField m_attachments;
    IntegerField m_comments;
    BooleanField m_isActive;
};
}

QDebug operator<<(QDebug dbg, const Database::NodeAttributesRecord &nodeAttributes);

#endif // DATABASE_NODEATTRIBUTESRECORD_H
