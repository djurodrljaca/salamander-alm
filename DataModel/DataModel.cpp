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

DataModel::DataModel::DataModel(QObject *parent)
    : QObject(parent),
      m_database(),
      m_projectList()
{
}

DataModel::DataModel::~DataModel()
{
    qDeleteAll(m_projectList);
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
        // Clear old data model
        emit modelAboutToBeReset();
        qDeleteAll(m_projectList);
        m_projectList.clear();

        // Load all "Project" nodes
        const QList<NodeRecord> nodeRecordList = m_database.getNodes(IntegerField(), &success);

        if (success)
        {
            foreach (const NodeRecord nodeRecordItem, nodeRecordList)
            {
                // Only "Project" nodes are allwed as root node
                if (nodeRecordItem.getType() != NodeType_Project)
                {
                    success = false;
                }

                // Load each found "Project" node
                if (success)
                {
                    Node *projectNode = new Node();
                    success = loadNodeFromDatabase(nodeRecordItem, NULL, projectNode);

                    if (success)
                    {
                        m_projectList.append(projectNode);
                        projectNode = NULL;
                    }
                    else
                    {
                        delete projectNode;
                        projectNode = NULL;
                        break;
                    }
                }
            }
        }

        emit modelReset();
    }

    return success;
}

int DataModel::DataModel::getProjectCount() const
{
    return m_projectList.size();
}

Node *DataModel::DataModel::getProject(const int index) const
{
    Node *project = NULL;

    if ((index >= 0) && (index < m_projectList.size()))
    {
        project = m_projectList[index];
    }

    return project;
}

int DataModel::DataModel::getProjectIndex(Node *projectNode) const
{
    int index = -1;

    if (projectNode != NULL)
    {
        index = m_projectList.indexOf(projectNode);
    }

    return index;
}

bool DataModel::DataModel::addNode(const Node &node)
{
    // Only single node items are allowed to be added
    bool success = (node.getChildCount() == 0);

    if (success)
    {
        Node *parent = node.getParent();

        if (parent == NULL)
        {
            // Only "Project" nodes are allowed as root items
            success = (node.getType() == Database::NodeType_Project);
        }
        else
        {
            // Check if the node's parent is contained in this data model
            success = contains(parent);
        }

        // Add node
        if (success)
        {
            // Prepare node record
            IntegerField parentId;

            if (parent != NULL)
            {
                parentId = parent->getId();
            }

            NodeRecord nodeRecord;
            nodeRecord.setParent(parentId);
            nodeRecord.setType(node.getType());

            // Add node record to database
            Node *insertedNode = NULL;
            IntegerField id;
            success = m_database.addNode(nodeRecord, &id);

            if (success)
            {
                insertedNode = new Node(node);
                insertedNode->setId(id);

                emit nodeAboutToBeAdded(parent);

                if (parent == NULL)
                {
                    m_projectList.append(insertedNode);
                }
                else
                {
                    parent->addChild(insertedNode);
                }

                emit nodeAdded();
            }
        }
    }

    return success;
}

bool DataModel::DataModel::loadNodeFromDatabase(const NodeRecord &nodeRecord,
                                                Node *parent,
                                                Node *node) const
{
    // Check if input parameters are valid
    bool success = (nodeRecord.isValid() &&
                    (node != NULL));

    if (success)
    {
        // Both node record's parent and the parent node must be compatible: both have to be null or
        // both have to be not null
        const bool isParentNull = (parent == NULL);
        success = (nodeRecord.getParent().isNull() == isParentNull);
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
                Node *childNode = new Node();
                success = loadNodeFromDatabase(nodeRecordItem, node, childNode);

                if (success)
                {
                    success = node->addChild(childNode);
                    childNode = NULL;
                }

                if (!success)
                {
                    break;
                }
            }
        }
    }

    return success;
}

bool DataModel::DataModel::contains(Node *node) const
{
    bool success = false;

    if (node != NULL)
    {
        Node *parent = node->getParent();

        if (parent == NULL)
        {
            success = m_projectList.contains(node);
        }
        else
        {
            success = contains(parent);
        }
    }

    return success;
}
