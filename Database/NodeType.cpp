/**
 * @file   NodeType.cpp
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

#include "Database/NodeType.h"
#include <QtCore/QString>

bool Database::isNodeTypeValid(const NodeType nodeType)
{
    bool valid = false;

    switch (nodeType)
    {
        case NodeType_Project:
        {
            valid = true;
            break;
        }

        default:
        {
            break;
        }
    }

    return valid;
}

Database::Integer Database::convertNoteTypeToInteger(const NodeType nodeType, bool *ok)
{
    Integer integer;
    bool success = false;

    if (isNodeTypeValid(nodeType))
    {
        integer.setValue(static_cast<qlonglong>(nodeType));
        success = true;
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return integer;
}

Database::NodeType Database::convertIntegerToNoteType(const Integer &integer, bool *ok)
{
    bool success = false;
    NodeType nodeType = NodeType_Invalid;

    if (!integer.isNull())
    {
        const NodeType value = static_cast<NodeType>(integer.getValue());

        if (isNodeTypeValid(value))
        {
            nodeType = value;
            success = true;
        }
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return nodeType;
}

QDebug operator<<(QDebug dbg, const Database::NodeType nodeType)
{
    switch (nodeType)
    {
        case Database::NodeType_Project:
        {
            dbg.nospace() << "Project";
            break;
        }

        case Database::NodeType_Invalid:
        default:
        {
            dbg.nospace() << "Invalid";
            break;
        }
    }

    return dbg.space();
}
