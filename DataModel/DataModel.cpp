/**
 * @file   TreeViewModel.cpp
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-5-29
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

using namespace Database;
using namespace DataModel;

DataModel::DataModel::DataModel()
    : m_database(),
      m_nodeList(),
      m_revisionId(),
      m_userId()
{
}

DataModel::DataModel::~DataModel()
{
    // Delete all items in the node list
    qDeleteAll(m_nodeList);
}

bool DataModel::DataModel::start()
{
    // Connect to the database
    bool success = m_database.isConnected();

    if (!success)
    {
        success = m_database.connect();
    }

    // Validate database
    if (success)
    {
        success = m_database.validate();

        if (!success)
        {
            // TODO: this probably needs to be removed later
            success = m_database.create();
        }
    }

    // On error stop the data model
    if (!success)
    {
        stop();
    }

    return success;
}

void DataModel::DataModel::stop()
{
    // Disconnect from the database
    if (m_database.isConnected())
    {
        m_database.disconnect();
    }
}

bool DataModel::DataModel::load(const IntegerField &requestedRevisionId)
{
    bool success = m_database.isConnected();

    if (success)
    {
        // Get current revision ID of the database
        const IntegerField currentRevisionId = m_database.getCurrentRevisionId(&success);

        if (success)
        {
            if (currentRevisionId.isNull())
            {
                success = false;
            }
        }

        // Get revision ID
        IntegerField revisionId;

        if (success)
        {
            if (requestedRevisionId.isNull())
            {
                // Selected the current revision of the database
                revisionId = currentRevisionId;
            }
            else if (requestedRevisionId.getValue() <= currentRevisionId.getValue())
            {
                // Selected the requested revision
                revisionId = requestedRevisionId;
            }
            else
            {
                // Invalid revision was requested
                success = false;
            }
        }

        // Clear old data model
        if (success && !m_nodeList.isEmpty())
        {
            qDeleteAll(m_nodeList);
            m_nodeList.clear();
        }

        // Load all root nodes that belong to the selected revision
        if (success)
        {
            const QList<NodeRecord> rootNodeRecordList = m_database.getNodes(IntegerField(),
                                                                             &success);

            if (success)
            {
                // Load each root node from the list
                foreach (const NodeRecord rootNodeRecordItem, rootNodeRecordList)
                {
                    // Load root node from the database
                    Node *rootNode = new Node();
                    success = loadNodeFromDatabase(rootNodeRecordItem, revisionId, NULL, rootNode);

                    if (success)
                    {
                        // Add only valid root nodes to the list
                        if (rootNode->isValid())
                        {
                            m_nodeList.append(rootNode);
                        }
                        else
                        {
                            delete rootNode;
                        }

                        rootNode = NULL;
                    }
                    else
                    {
                        // Error
                        delete rootNode;
                        rootNode = NULL;
                        break;
                    }
                }
            }
        }

        // Set the data model revision
        if (success)
        {
            m_revisionId = revisionId;
        }
    }

    return success;
}

bool DataModel::DataModel::login(const QString &username, const QString &password)
{
    // Check input parameters
    bool success = (!username.isEmpty() &&
                    !password.isEmpty());

    // Get user record from username
    if (success)
    {
        const UserRecord userRecord = m_database.getUser(username, &success);

        if (success)
        {
            // Error, invalid username
            success = userRecord.isValid();
        }

        if (success)
        {
            if ((username == userRecord.getUsername().getValue()) &&
                (password == userRecord.getPassword().getValue()))
            {
                // Login successful
                m_userId = userRecord.getId();
            }
            else
            {
                // Error, invalid username or password
                success = false;
            }
        }
    }

    return success;
}

bool DataModel::DataModel::loadNodeFromDatabase(const NodeRecord &nodeRecord,
                                                const IntegerField &revisionId,
                                                Node *parent,
                                                Node *node)
{
    // Check if input parameters are valid
    bool success = (nodeRecord.isValid() &&
                    (node != NULL));

    // Chack parents
    if (success)
    {
        if (parent == NULL)
        {
            // If the parent parameter is null then also the node parent must be null
            if (!nodeRecord.getParent().isNull())
            {
                success = false;
            }
        }
        else if (parent->getId().isNull())
        {
            // Parent parameter ID must not be null
            success = false;
        }
        else
        {
            // Both parent ID's must match
            if (nodeRecord.getParent() != parent->getId())
            {
                success = false;
            }
        }
    }

    // Start loading node from the database
    if (success)
    {
        // Get node attributes
        const IntegerField nodeAttributesId = m_database.getNodeAttributesId(nodeRecord.getId(),
                                                                             revisionId,
                                                                             &success);

        if (success)
        {
            const NodeAttributesRecord nodeAttributesRecord =
                    m_database.getNodeAttributes(nodeAttributesId, &success);

            if (success)
            {
                success = nodeAttributesRecord.isValid();
            }

            if (success)
            {
                const bool isActive = nodeAttributesRecord.getIsActive().getValue();

                if (isActive)
                {
                    // Get node name
                    const NodeNameRecord nodeNameRecord =
                            m_database.getNodeName(nodeAttributesRecord.getName(), &success);

                    if (success)
                    {
                        success = nodeNameRecord.isValid();
                    }

                    // Set output node's parameters
                    if (success)
                    {
                        node->setId(nodeRecord.getId());
                        node->setParent(parent);
                        node->setType(nodeRecord.getType());

                        node->setRevisionId(nodeAttributesRecord.getRevision());
                        node->setName(nodeNameRecord.getText().getValue());
                        node->setDescriptionId(nodeAttributesRecord.getDescription());
                        node->setReferencesId(nodeAttributesRecord.getReferences());
                        node->setAttachmentsId(nodeAttributesRecord.getAttachments());
                        node->setCommentsId(nodeAttributesRecord.getComments());

                        // Load child nodes
                        success = loadChildNodesFromDatabase(revisionId, node);
                    }
                }
                else
                {
                    // Node is inactive, make sure the output node is invalidated
                    node->setId(IntegerField());
                }
            }
        }
    }

    return success;
}

bool DataModel::DataModel::loadChildNodesFromDatabase(const IntegerField &revisionId, Node *parent)
{
    bool success = false;

    // Get list of all child nodes
    const QList<NodeRecord> childNodeRecordList = m_database.getNodes(parent->getId(), &success);

    if (success)
    {
        foreach (const Database::NodeRecord childNodeRecordItem, childNodeRecordList)
        {
            // Load child node from the database and add it to the parent node
            Node *child = new Node();
            success = loadNodeFromDatabase(childNodeRecordItem, revisionId, parent, child);

            if (success)
            {
                // Add only valid child nodes to the parent
                if (child->isValid())
                {
                    success = parent->addChild(child);
                }
                else
                {
                    delete child;
                }

                child = NULL;
            }

            if (!success)
            {
                // Error
                delete child;
                child = NULL;
                break;
            }
        }
    }

    return success;
}
