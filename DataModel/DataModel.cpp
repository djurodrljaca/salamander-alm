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
#include "Database/NodeRecord.h"

using namespace DataModel;
using namespace Database;

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
        // Load all root nodes - only "Project" nodes are allowed to be root nodes!
        const QList<NodeRecord> nodeRecordList = m_database.getNodes(IntegerField(), &success);

        if (success)
        {
            foreach (const NodeRecord nodeRecordItem, nodeRecordList)
            {
                // TODO: check if all root nodes are "Project" nodes!
                // Load each found "Project" node
                Node node;
                success = loadNodeFromDatabase(nodeRecordItem, &node);

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

bool DataModel::DataModel::loadNodeFromDatabase(const NodeRecord &nodeRecord,
                                                Node *node,
                                                Node *parent) const
{
    // Check if input parameters are valid
    bool success = (nodeRecord.isValid() &&
                    (node != NULL));

    if (success)
    {
        // Both node record's parent and the parent node must be compatible: both have to be null or
        // both have to be not null
        success = (nodeRecord.getParent().isNull() == (parent == NULL));
    }

    if (success)
    {
        // Set node parameters
        node->setId(nodeRecord.getId());
        node->setParent(parent);
        node->setType(nodeRecord.getType());

        // Load child nodes and add them to the node
        const QList<NodeRecord> nodeRecordList = m_database.getNodes(nodeRecord.getId(), &success);

        if (success)
        {
            foreach (const Database::NodeRecord nodeRecordItem, nodeRecordList)
            {
                // Load child node and add it to the node
                Node childNode;
                success = loadNodeFromDatabase(nodeRecordItem, &childNode, node);


                if (success)
                {
                    node->addChild(childNode);
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
