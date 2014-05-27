/**
 * @file   NodeType.h
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-5-24
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

#ifndef DATABASE_NODETYPE_H
#define DATABASE_NODETYPE_H

#include "Database/Integer.h"
#include <QtCore/QDebug>

namespace Database
{

// TODO: move to DataModel?

enum NodeType
{
    NodeType_Invalid = 0,
    NodeType_Project
};

bool isNodeTypeValid(const NodeType nodeType);
Integer convertNoteTypeToInteger(const NodeType nodeType, bool *ok = NULL);
NodeType convertIntegerToNoteType(const Integer &integer, bool *ok = NULL);

}

QDebug operator<<(QDebug dbg, const Database::NodeType nodeType);

#endif // DATABASE_NODETYPE_H
