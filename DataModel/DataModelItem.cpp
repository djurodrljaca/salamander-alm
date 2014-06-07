/**
 * @file   DataModelItem.cpp
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-06-07
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

#include "DataModel/DataModelItem.h"

using namespace DataModel;
using namespace Database;

DataModelItem::DataModelItem()
    : m_id(),
      m_parent(NULL),
      m_type(NodeType_Invalid),
      m_revisionId(),
      m_name(),
      m_descriptionId(),
      m_referencesId(),
      m_attachmentsId(),
      m_commentsId(),
      m_childList()
{
}

DataModelItem::~DataModelItem()
{
    qDeleteAll(m_childList);
}

bool DataModelItem::isValid() const
{
    return (isNodeTypeValid(m_type) &&
            !m_revisionId.isNull() &&
            !m_name.isEmpty());
}

IntegerField DataModelItem::getId() const
{
    return m_id;
}

void DataModelItem::setId(const IntegerField &id)
{
    m_id = id;
}

DataModelItem * DataModelItem::getParent() const
{
    return m_parent;
}

void DataModelItem::setParent(DataModelItem *parent)
{
    m_parent = parent;
}

NodeType DataModelItem::getType() const
{
    return m_type;
}

void DataModelItem::setType(const NodeType type)
{
    m_type = type;
}

IntegerField DataModelItem::getRevisionId() const
{
    return m_revisionId;
}

void DataModelItem::setRevisionId(const IntegerField &revisionId)
{
    m_revisionId = revisionId;
}

QString DataModelItem::getName() const
{
    return m_name;
}

void DataModelItem::setName(const QString &name)
{
    m_name = name;
}

IntegerField DataModelItem::getDescriptionId() const
{
    return m_descriptionId;
}

void DataModelItem::setDescriptionId(const IntegerField &descriptionId)
{
    m_descriptionId = descriptionId;
}

IntegerField DataModelItem::getReferencesId() const
{
    return m_referencesId;
}

void DataModelItem::setReferencesId(const IntegerField &referencesId)
{
    m_referencesId = referencesId;
}

IntegerField DataModelItem::getAttachmentsId() const
{
    return m_attachmentsId;
}

void DataModelItem::setAttachmentsId(const IntegerField &attachmentsId)
{
    m_attachmentsId = attachmentsId;
}

IntegerField DataModelItem::getCommentsId() const
{
    return m_commentsId;
}

void DataModelItem::setCommentsId(const IntegerField &commentsId)
{
    m_commentsId = commentsId;
}

int DataModelItem::getChildCount() const
{
    return m_childList.size();
}

DataModelItem * DataModelItem::getChild(const int index) const
{
    DataModelItem *child = NULL;

    if ((index >= 0) && (index < m_childList.size()))
    {
        child = m_childList[index];
    }

    return child;
}

int DataModelItem::getChildIndex(DataModelItem * const child) const
{
    return m_childList.indexOf(child);
}

bool DataModelItem::addChild(DataModelItem *child)
{
    bool success = false;

    if (child != NULL)
    {
        m_childList.append(child);
        success = true;
    }

    return success;
}
