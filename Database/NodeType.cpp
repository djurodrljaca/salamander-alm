/**
 * @file   NodeType.cpp
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-05-24
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

using namespace Database;

bool Database::isNodeTypeValid(const NodeType nodeType)
{
    bool valid = false;

    switch (nodeType)
    {
        case NodeType_Project:
        case NodeType_Requirement:
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

IntegerField Database::convertNodeTypeToInteger(const NodeType nodeType, bool *ok)
{
    IntegerField integer;
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

NodeType Database::convertIntegerToNodeType(const IntegerField &integer, bool *ok)
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
        success = true;
    {
        *ok = success;
    }

    return nodeType;
}

QDebug operator<<(QDebug dbg, const NodeType nodeType)
{
    dbg.nospace() << convertNodeTypeToString(nodeType);
    return dbg.space();
}

QString Database::convertNodeTypeToString(const NodeType nodeType, bool *ok)
{
    bool success = false;
    QString value;

    switch (nodeType)
    {
        case NodeType_Project:
        {
            value = "Project";
            success = true;
            break;
        }

        case NodeType_Requirement:
        {
            value = "Requirement";
            success = true;
            break;
        }

        case NodeType_Invalid:
        default:
        {
            value = "Invalid";
            break;
        }
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return value;
}

NodeType Database::convertStringToNodeType(const QString &value, bool *ok)
{
    bool success = false;
    NodeType nodeType;

    if (value == QString("Project"))
    {
        nodeType = NodeType_Project;
        success = true;
    }
    else if (value == QString("Requirement"))
    {
        nodeType = NodeType_Requirement;
        success = true;
    }
    else
    {
        nodeType = NodeType_Invalid;
    }

    if (ok != NULL)
    {
        *ok = success;
    }

    return nodeType;
}
