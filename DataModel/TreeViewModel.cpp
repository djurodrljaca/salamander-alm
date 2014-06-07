/**
 * @file   TreeViewModel.cpp
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-05-29
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
using namespace DataModel;

TreeViewModel::TreeViewModel(QObject *parent)
    : QAbstractItemModel(parent),
      m_dataModel()
{
}

TreeViewModel::~TreeViewModel()
{
}

bool DataModel::TreeViewModel::start()
{
    return m_dataModel.start();
}

void DataModel::TreeViewModel::stop()
{
    m_dataModel.stop();
}

bool DataModel::TreeViewModel::load()
{
    // Notify the view that the data model will be reset
    beginResetModel();

    // Load data model
    bool success = m_dataModel.load(); // TODO: add a parameter for loading a specific revision?

    // Notify the view that the data model reset has finished
    endResetModel();

    return success;
}

bool TreeViewModel::login(const QString &username, const QString &password)
{
    return m_dataModel.login(username, password);
}

bool TreeViewModel::addProject(const QString &name, const QString &description)
{
    // Notify the view that a row is about to be inserted
    int row = m_dataModel.getRootItemCount();
    beginInsertRows(QModelIndex(), row, row);

    // Add node to the model
    bool success = m_dataModel.addItem(IntegerField(), NodeType_Project, name, description);

    row = m_dataModel.getRootItemCount();

    // Notify the view that row insertion has finished
    endInsertRows();

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

DataModelItem *DataModel::TreeViewModel::getDataModelItem(const QModelIndex &index) const
{
    return static_cast<DataModelItem *>(index.internalPointer());
}

QVariant DataModel::TreeViewModel::data(const QModelIndex &index, int role) const
{
    QVariant dataValue;

    if (index.isValid() &&
        (role == Qt::DisplayRole))
    {
        // Set the data value to the item's name
        const DataModelItem *item = getDataModelItem(index);

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
    // Create model index
    QModelIndex modelIndex;

    if (hasIndex(row, column, parent))
    {
        // Get item from the data model
        DataModelItem *item = NULL;

        if (!parent.isValid())
        {
            // Parent model index is invalid, return a root item with index "row"
            item = m_dataModel.getRootItem(row);
        }
        else
        {
            // Get parent data model item from the parent model index
            const DataModelItem *parentItem = getDataModelItem(parent);

            if (parentItem != NULL)
            {
                // Parent data model item is valid, return a child item with index "row"
                item = parentItem->getChild(row);
            }
        }

        // Create model index if item is valid
        if (item != NULL)
        {
            modelIndex = createIndex(row, column, item);
        }
    }

    return modelIndex;
}

QModelIndex DataModel::TreeViewModel::parent(const QModelIndex &index) const
{
    // Get a parent model index from the selected model index
    QModelIndex modelIndex;

    if (index.isValid())
    {
        // Get the (child) data model item from the selected index
        const DataModelItem *childItem = getDataModelItem(index);

        if (childItem != NULL)
        {
            // Get the parent model item from its child model item
            int parentRow = 0;
            DataModelItem *parentItem = childItem->getParent();

            if (parentItem != NULL)
            {
                // Child model item has a parent, create a model index for it
                parentRow = getItemRow(parentItem);
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

    if (column <= 0)
    {
        if (!parent.isValid())
        {
            // Number of root items was requested
            count = m_dataModel.getRootItemCount();
        }
        else
        {
            // Number of children for the selected parent was requested
            DataModelItem *parentItem = getDataModelItem(parent);

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
    // We only have one column in this view
    return 1;
}

int TreeViewModel::getItemRow(DataModelItem *item) const
{
    int row = 0;

    if (item != NULL)
    {
        const DataModelItem *parentItem = item->getParent();

        if (parentItem == NULL)
        {
            row = m_dataModel.getRootItemIndex(item);
        }
        else
        {
            row = parentItem->getChildIndex(item);
        }
    }

    return row;
}
