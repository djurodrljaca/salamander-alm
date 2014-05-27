/**
 * @file   DataModel.cpp
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

#include "DataModel/DataModel.h"
#include "Database/Node.h"

DataModel::DataModel::DataModel()
    : m_database(),
      m_nodeList()
{
}

bool DataModel::DataModel::start()
{
    bool success = false;

    if (m_database.isConnected() == false)
    {
        success = m_database.connect();

        if (success)
        {
            success = m_database.validate();

            if (!success)
            {
                // TODO: this probably needs to be removed later
                success = m_database.create();

                if (!success)
                {
                    m_database.disconnect();
                }
            }
        }
    }

    return success;
}

void DataModel::DataModel::stop()
{
    if (m_database.isConnected())
    {
        m_database.disconnect();
    }
}

bool DataModel::DataModel::load()
{
    bool success = m_database.isConnected();

    if (success)
    {
        const QList<Database::Node> databaseNodeList =
                m_database.getNodes(Database::Integer(), &success);

        if (success)
        {
            foreach (const Database::Node databaseNodeItem, databaseNodeList)
            {
                Node node;
                node.setParent(NULL);

                success = loadNodeFromDatabase(databaseNodeItem.getId(), &node);

                if (success)
                {
                    m_nodeList.append(node);
                }
                else
                {
                    break;
                }
            }
        }
    }

    return success;
}

bool DataModel::DataModel::loadNodeFromDatabase(const Database::Integer &id, Node *parent) const
{
    bool success = (parent != NULL);

    if (success)
    {
        const QList<Database::Node> databaseNodeList = m_database.getNodes(id, &success);

        if (success)
        {
            Node childNode;

            if (databaseNodeList.isEmpty())
            {
                Database::Node databaseNode = m_database.getNode(id, &success);

                if (success)
                {
                    if (parent->getId() == databaseNode.getParent())
                    {
                        childNode.setId(databaseNode.getId());
                        childNode.setParent(parent);
                        childNode.setType(databaseNode.getType());
                    }
                    else
                    {
                        success = false;
                    }
                }
            }
            else
            {
                foreach (const Database::Node databaseNodeItem, databaseNodeList)
                {
                    childNode = loadNodeFromDatabase(databaseNodeItem.getId(), &success);

                    if (!success)
                    {
                        break;
                    }
                }
            }

            if (success)
            {
                parent->addChild(childNode);
            }
        }
    }

    return success;
}
