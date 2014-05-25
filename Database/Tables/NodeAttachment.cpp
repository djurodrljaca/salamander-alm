/**
 * @file   NodeAttachment.cpp
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

#include "Database/Tables/NodeAttachment.h"

using namespace Database::Tables;
using namespace Database::DataTypes;

NodeAttachment::NodeAttachment()
    : m_id(),
      m_fileName(),
      m_fileData()
{
}

NodeAttachment::NodeAttachment(const Integer &id,
                               const Text &fileName,
                               const Blob &fileData)
    : m_id(id),
      m_fileName(fileName),
      m_fileData(fileData)
{
}

bool NodeAttachment::isValid() const
{
    return (!m_id.isNull() &&
            !m_fileName.isNull() &&
            !m_fileData.isNull());
}

Integer NodeAttachment::getId() const
{
    return m_id;
}

void NodeAttachment::setId(const Integer &id)
{
    m_id = id;
}

Text NodeAttachment::getFileName() const
{
    return m_fileName;
}

void NodeAttachment::setFileName(const Text &fileName)
{
    m_fileName = fileName;
}

Blob NodeAttachment::getFileData() const
{
    return m_fileData;
}

void NodeAttachment::setFileData(const Blob &fileData)
{
    m_fileData = fileData;
}

NodeAttachment NodeAttachment::fromRecord(const QSqlRecord &record, bool *ok)
{
    NodeAttachment nodeAttachment;
    bool success = !record.isEmpty();

    // Id
    if (success)
    {
        nodeAttachment.setId(Integer::fromField(record.field("Id"), &success));
    }

    // FileName
    if (success)
    {
        nodeAttachment.setFileName(Text::fromField(record.field("FileName"), &success));
    }

    // FileData
    if (success)
    {
        nodeAttachment.setFileData(Text::fromField(record.field("FileData"), &success));
    }

    // Check NodeAttachment
    if (!success ||
        !nodeAttachment.isValid())
    {
        nodeAttachment = NodeAttachment();
        success = false;
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return nodeAttachment;
}
