/**
 * @file   NodeDescriptionRecord.h
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

#ifndef DATABASE_NODEDESCRIPTIONRECORD_H
#define DATABASE_NODEDESCRIPTIONRECORD_H

#include "Database/IntegerField.h"
#include "Database/TextField.h"
#include <QtCore/QtDebug>

namespace Database
{
class NodeDescriptionRecord
{
public:
    NodeDescriptionRecord();
    NodeDescriptionRecord(const IntegerField &id,
                          const TextField &text);

    bool isValid() const;

    IntegerField getId() const;
    void setId(const IntegerField &id);

    TextField getText() const;
    void setText(const TextField &text);

private:
    IntegerField m_id;
    TextField m_text;
};
}

QDebug operator<<(QDebug dbg, const Database::NodeDescriptionRecord &nodeDescription);

#endif // DATABASE_NODEDESCRIPTIONRECORD_H
