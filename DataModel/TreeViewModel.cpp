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

#include "TreeViewModel.h"

using namespace Database;

DataModel::TreeViewModel::TreeViewModel(QObject *parent)
    : QAbstractItemModel(parent),
      m_database(),
      m_projectList()
{
}

DataModel::TreeViewModel::~TreeViewModel()
{
    qDeleteAll(m_projectList);
}

bool DataModel::TreeViewModel::start()
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

void DataModel::TreeViewModel::stop()
{
    if (m_database.isConnected())
    {
        m_database.disconnect();
    }
}

bool DataModel::TreeViewModel::load()
{
    bool success = m_database.isConnected();

    if (success)
    {
        // Clear old data model
        beginResetModel();
        qDeleteAll(m_projectList);
        m_projectList.clear();

        // Load all "Project" nodes
        const QList<NodeRecord> nodeRecordList = m_database.getNodes(IntegerField(), &success);
        IntegerField currentRevisionId;

        if (success)
        {
            currentRevisionId = m_database.getCurrentRevisionId(&success);
        }

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
                    bool isActive = false;

                    success = loadNodeFromDatabase(nodeRecordItem,
                                                   currentRevisionId,
                                                   NULL,
                                                   projectNode,
                                                   &isActive);

                    if (success)
                    {
                        if (isActive)
                        {
                            m_projectList.append(projectNode);
                        }
                        else
                        {
                            delete projectNode;
                        }

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

        endResetModel();
    }

    return success;
}

bool DataModel::TreeViewModel::addProject(const QString &name, const QString description)
{
    bool success = !name.isEmpty();

    if (success)
    {
        // TODO: check if project with the same name already exists

        // Start revision
        IntegerField revisionId = m_database.startRevision(&success);

        // Add node record
        IntegerField nodeId;
        NodeRecord nodeRecord;
        nodeRecord.setParent(IntegerField());
        nodeRecord.setType(NodeType_Project);

        success = m_database.addNode(nodeRecord, &nodeId);

        // Add node name
        IntegerField nodeNameId;

        if (success)
        {
            const NodeNameRecord nodeName(IntegerField(), name);
            success = m_database.addNodeName(nodeName, &nodeNameId);
        }

        // Add node description
        IntegerField nodeDescriptionId;

        if (success && !description.isEmpty())
        {
            const NodeDescriptionRecord nodeDescription(IntegerField(), description);
            success = m_database.addNodeDescription(nodeDescription, &nodeDescriptionId);
        }

        // Add node attributes
        IntegerField nodeAttributesId;

        if (success)
        {
            const NodeAttributesRecord nodeAttributes(IntegerField(),
                                                      nodeId,
                                                      revisionId,
                                                      nodeNameId,
                                                      nodeDescriptionId,
                                                      IntegerField(),
                                                      IntegerField(),
                                                      IntegerField(),
                                                      BooleanField(true));
            success = m_database.addNodeAttributes(nodeAttributes, &nodeAttributesId);
        }

        if (success)
        {
            success = m_database.finishRevision();
            // TODO: refresh data model (tree view)
        }
        else
        {
            m_database.abortRevision();
        }
    }

    return success;
}

//bool DataModel::TreeViewModel::addNode(const QModelIndex &parent, const DataModel::Node &node)
//{
//    // Only single node items are allowed to be added
//    bool success = (node.getChildCount() == 0);

//    if (success)
//    {
//        Node *parentItem = getNode(parent);

//        if (parentItem == NULL)
//        {
//            // Only "Project" nodes are allowed as root items
//            success = (node.getType() == Database::NodeType_Project);
//        }
//        else
//        {
//            // Check if the node's parent is contained in this data model
//            success = contains(parentItem);
//        }

//        // Add node
//        if (success)
//        {
//            // Start revision
//            IntegerField revisionId = m_database.startRevision(&success);

//            // Prepare node record
//            if (success)
//            {
//                IntegerField parentId;

//                if (parentItem != NULL)
//                {
//                    parentId = parentItem->getId();
//                }

//                NodeRecord nodeRecord;
//                nodeRecord.setParent(parentId);
//                nodeRecord.setType(node.getType());

//                // Add node record to database
//                Node *insertedNode = NULL;
//                IntegerField id;
//                success = m_database.addNode(nodeRecord, &id);

//                // Create node
//                if (success)
//                {
//                    insertedNode = new Node(node);
//                    insertedNode->setId(id);
//                    insertedNode->setParent(parentItem);
//                }

//                if (success)
//                {
//                    success = m_database.finishRevision();

//                    // Add node to the model
//                    if (parentItem == NULL)
//                    {
//                        int row = m_projectList.size();
//                        beginInsertRows(parent, row, row);

//                        m_projectList.append(insertedNode);
//                        insertedNode = NULL;
//                    }
//                    else
//                    {
//                        int row = parentItem->getChildCount();
//                        beginInsertRows(parent, row, row);

//                        parentItem->addChild(insertedNode);
//                        insertedNode = NULL;
//                    }

//                    endInsertRows();
//                }
//                else
//                {
//                    m_database.abortRevision();
//                }
//            }
//        }
//    }

//    return success;
//}

DataModel::Node *DataModel::TreeViewModel::getNode(const QModelIndex &index) const
{
    return static_cast<Node *>(index.internalPointer());
}

QVariant DataModel::TreeViewModel::data(const QModelIndex &index, int role) const
{
    QVariant dataValue;

    if (index.isValid() &&
        (role == Qt::DisplayRole))
    {
        const Node *item = getNode(index);

        if (item != NULL)
        {
            const QString name = item->getName();

            if (name.isEmpty())
            {
                dataValue = QVariant(QString("???"));
            }
            else
            {
                dataValue = QVariant(name);
            }
        }
    }

    return dataValue;
}

Qt::ItemFlags DataModel::TreeViewModel::flags(const QModelIndex &index) const
{
    Qt::ItemFlags value = 0;

    if (index.isValid())
    {
        value = Qt::ItemIsEnabled | Qt::ItemIsSelectable;
    }

    return value;
}

QModelIndex DataModel::TreeViewModel::index(int row, int column, const QModelIndex &parent) const
{
    QModelIndex modelIndex;

    if (hasIndex(row, column, parent) &&
        m_database.isConnected())
    {
        Node *item = NULL;

        if (!parent.isValid())
        {
            item = getProject(row);
        }
        else
        {
            const Node *parentItem = getNode(parent);

            if (parentItem != NULL)
            {
                item = parentItem->getChild(row);
            }
        }

        if (item != NULL)
        {
            modelIndex = createIndex(row, column, item);
        }
    }

    return modelIndex;
}

QModelIndex DataModel::TreeViewModel::parent(const QModelIndex &index) const
{
    QModelIndex modelIndex;

    if (index.isValid() &&
        m_database.isConnected())
    {
        const Node *childItem = getNode(index);

        if (childItem != NULL)
        {
            int parentRow = 0;
            Node *parentItem = childItem->getParent();

            if (parentItem != NULL)
            {
                parentRow = getNodeRow(parentItem);
                modelIndex = createIndex(parentRow, 0, parentItem);
            }
        }
    }

    return modelIndex;
}

int DataModel::TreeViewModel::rowCount(const QModelIndex &parent) const
{
    int count = 0;
    const int column = parent.column();

    if ((column <= 0) &&
        m_database.isConnected())
    {
        if (!parent.isValid())
        {
            count = getProjectCount();
        }
        else
        {
            Node *parentItem = getNode(parent);

            if (parentItem != NULL)
            {
                count = parentItem->getChildCount();
            }
        }
    }

    return count;
}

int DataModel::TreeViewModel::columnCount(const QModelIndex &) const
{
    // TODO: implement correctly
    return 1;
}

int DataModel::TreeViewModel::getProjectCount() const
{
    return m_projectList.size();
}

DataModel::Node *DataModel::TreeViewModel::getProject(const int index) const
{
    Node *project = NULL;

    if ((index >= 0) && (index < m_projectList.size()))
    {
        project = m_projectList[index];
    }

    return project;
}

int DataModel::TreeViewModel::getProjectIndex(DataModel::Node *projectNode) const
{
    int index = -1;

    if (projectNode != NULL)
    {
        index = m_projectList.indexOf(projectNode);
    }

    return index;
}

int DataModel::TreeViewModel::getNodeRow(DataModel::Node *node) const
{
    // TODO: is this still needed? fix it?
    int row = 0;

    if (node != NULL)
    {
        const Node *parentItem = node->getParent();

        if (parentItem == NULL)
        {
            row = getProjectIndex(node);
        }
        else
        {
            row = parentItem->getChildIndex(node);
        }
    }

    return row;
}

bool DataModel::TreeViewModel::loadNodeFromDatabase(const NodeRecord &nodeRecord,
                                                    const IntegerField &revisionId,
                                                    DataModel::Node *parent,
                                                    DataModel::Node *node,
                                                    bool *isActive) const
{
    // Check if input parameters are valid
    bool success = (nodeRecord.isValid() &&
                    (node != NULL) &&
                    (isActive != NULL));

    if (success)
    {
        // Both node record's parent and the parent node must be compatible: both have to be null or
        // both have to be not null
        const bool isParentNull = (parent == NULL);
        success = (nodeRecord.getParent().isNull() == isParentNull);
    }

    if (success)
    {
        // Get note attributes
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
                *isActive = nodeAttributesRecord.getIsActive().getValue();

                if (*isActive)
                {
                    // Get node name
                    const NodeNameRecord nodeNameRecord =
                            m_database.getNodeName(nodeAttributesRecord.getName(), &success);

                    if (success)
                    {
                        success = nodeNameRecord.isValid();
                    }

                    // Set node parameters
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
                    }
                }
            }
        }

        // Load child nodes and add them to the node
        if (success && *isActive)
        {
            const QList<NodeRecord> nodeRecordList = m_database.getNodes(nodeRecord.getId(), &success);

            if (success)
            {
                foreach (const Database::NodeRecord nodeRecordItem, nodeRecordList)
                {
                    // Load child node and add it to the node
                    Node *childNode = new Node();
                    bool isChildActive = false;

                    success = loadNodeFromDatabase(nodeRecordItem,
                                                   revisionId,
                                                   node,
                                                   childNode,
                                                   &isChildActive);

                    if (success)
                    {
                        if (isChildActive)
                        {
                            success = node->addChild(childNode);
                        }
                        else
                        {
                            delete childNode;
                        }

                        childNode = NULL;
                    }

                    if (!success)
                    {
                        break;
                    }
                }
            }
        }
    }

    return success;
}

bool DataModel::TreeViewModel::contains(DataModel::Node *node) const
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
