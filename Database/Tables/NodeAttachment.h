/**
 * @file   NodeAttachment.h
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

#ifndef DATABASE_TABLES_NODEATTACHMENT_H
#define DATABASE_TABLES_NODEATTACHMENT_H

#include "Database/DataTypes/Blob.h"
#include "Database/DataTypes/Integer.h"
#include "Database/DataTypes/Text.h"
#include <QtSql/QSqlRecord>

namespace Database
{
namespace Tables
{
class NodeAttachment
{
public:
    NodeAttachment();
    NodeAttachment(const DataTypes::Integer &id,
                   const DataTypes::Text &fileName,
                   const DataTypes::Blob &fileData);

    bool isValid() const;

    DataTypes::Integer getId() const;
    void setId(const DataTypes::Integer &id);

    DataTypes::Text getFileName() const;
    void setFileName(const DataTypes::Text &fileName);

    DataTypes::Blob getFileData() const;
    void setFileData(const DataTypes::Blob &fileData);

    static NodeAttachment fromRecord(const QSqlRecord &record, bool *ok = NULL);

private:
    DataTypes::Integer m_id;
    DataTypes::Text m_fileName;
    DataTypes::Blob m_fileData;
};
}
}

#endif // DATABASE_TABLES_NODEATTACHMENT_H
