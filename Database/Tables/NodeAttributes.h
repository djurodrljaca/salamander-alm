/**
 * @file   NodeAttributes.h
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

#ifndef NODEATTRIBUTES_H
#define NODEATTRIBUTES_H

#include "Database/DataTypes/Boolean.h"
#include "Database/DataTypes/Integer.h"
#include <QtSql/QSqlRecord>

namespace Database
{
namespace Tables
{
class NodeAttributes
{
public:
    NodeAttributes();
    NodeAttributes(const DataTypes::Integer &id,
                   const DataTypes::Integer &node,
                   const DataTypes::Integer &revision,
                   const DataTypes::Integer &name,
                   const DataTypes::Integer &description,
                   const DataTypes::Integer &references,
                   const DataTypes::Integer &attachments,
                   const DataTypes::Integer &comments,
                   const DataTypes::Boolean &isActive);

    bool isValid() const;

    DataTypes::Integer getId() const;
    void setId(const DataTypes::Integer &id);

    DataTypes::Integer getNode() const;
    void setNode(const DataTypes::Integer &node);

    DataTypes::Integer getRevision() const;
    void setRevision(const DataTypes::Integer &revision);

    DataTypes::Integer getName() const;
    void setName(const DataTypes::Integer &name);

    DataTypes::Integer getDescription() const;
    void setDescription(const DataTypes::Integer &description);

    DataTypes::Integer getReferences() const;
    void setReferences(const DataTypes::Integer &references);

    DataTypes::Integer getAttachments() const;
    void setAttachments(const DataTypes::Integer &attachments);

    DataTypes::Integer getComments() const;
    void setComments(const DataTypes::Integer &comments);

    DataTypes::Boolean getIsActive() const;
    void setIsActive(const DataTypes::Boolean &isActive);

    static NodeAttributes fromRecord(const QSqlRecord &record, bool *ok = NULL);

private:
    DataTypes::Integer m_id;
    DataTypes::Integer m_node;
    DataTypes::Integer m_revision;
    DataTypes::Integer m_name;
    DataTypes::Integer m_description;
    DataTypes::Integer m_references;
    DataTypes::Integer m_attachments;
    DataTypes::Integer m_comments;
    DataTypes::Boolean m_isActive;
};
}
}

#endif // NODEATTRIBUTES_H
