/**
 * @file   ViewModel.cpp
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-05-28
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

#include "ViewModel.h"

using namespace DataModel;

ViewModel::ViewModel::ViewModel(QObject *parent)
    : QAbstractItemModel(parent),
      m_dataModel(NULL)
{
}

ViewModel::ViewModel::~ViewModel()
{
}

void ViewModel::ViewModel::setDataModel(DataModel::DataModel *dataModel)
{
    beginResetModel();

    if (m_dataModel != NULL)
    {
        disconnect(this, SLOT(dataModelAboutToReset()));
        disconnect(this, SLOT(dataModelReset()));

        disconnect(this, SLOT(nodeAboutToBeAdded(DataModel::Node*)));
        disconnect(this, SLOT(nodeAdded()));
    }

    m_dataModel = dataModel;

    if (m_dataModel != NULL)
    {
        connect(m_dataModel, SIGNAL(modelAboutToBeReset()), this, SLOT(dataModelAboutToReset()));
        connect(m_dataModel, SIGNAL(modelReset()), this, SLOT(dataModelReset()));

        connect(m_dataModel, SIGNAL(nodeAboutToBeAdded(const Node*)),
                this, SLOT(nodeAboutToBeAdded(DataModel::Node*)));
        connect(m_dataModel, SIGNAL(nodeAdded()), this, SLOT(nodeAdded()));
    }

    endResetModel();
}

QVariant ViewModel::ViewModel::data(const QModelIndex &index, int role) const
{
    QVariant dataValue;

    if (index.isValid() &&
        (role == Qt::DisplayRole))
    {
        // TODO: implement correctly

        const Node *item = getNode(index);

        if (item != NULL)
        {
            const Database::IntegerField id = item->getId();

            if (!id.isNull())
            {
                dataValue = QVariant(QString("Project: %1").arg(id.getValue()));
            }
        }
    }

    return dataValue;
}

Qt::ItemFlags ViewModel::ViewModel::flags(const QModelIndex &index) const
{
    Qt::ItemFlags value = 0;

    if (index.isValid())
    {
        value = Qt::ItemIsEnabled | Qt::ItemIsSelectable;
    }

    return value;
}

QModelIndex ViewModel::ViewModel::index(int row, int column, const QModelIndex &parent) const
{
    QModelIndex modelIndex;

    if (hasIndex(row, column, parent) &&
        (m_dataModel != NULL))
    {
        Node *item = NULL;

        if (!parent.isValid())
        {
            item = m_dataModel->getProject(row);
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

QModelIndex ViewModel::ViewModel::parent(const QModelIndex &index) const
{
    QModelIndex modelIndex;

    if (index.isValid() &&
        (m_dataModel != NULL))
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

int ViewModel::ViewModel::rowCount(const QModelIndex &parent) const
{
    int count = 0;
    const int column = parent.column();

    if ((column <= 0) &&
        (m_dataModel != NULL))
    {
        if (!parent.isValid())
        {
            count = m_dataModel->getProjectCount();
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

int ViewModel::ViewModel::columnCount(const QModelIndex &) const
{
    // TODO: implement correctly
    return 1;
}

void ViewModel::ViewModel::dataModelAboutToReset()
{
    beginResetModel();
}

void ViewModel::ViewModel::dataModelReset()
{
    endResetModel();
}

void ViewModel::ViewModel::nodeAboutToBeAdded(Node *parent)
{
    // TODO: check why this makes it crashes below!

    QModelIndex parentModelIndex;
    int insertRow = 0;

    if (parent != NULL)
    {
        int row = getNodeRow(parent);
        parentModelIndex = createIndex(row, 0, parent);
    }

    beginInsertRows(parentModelIndex, insertRow, insertRow);
}

void ViewModel::ViewModel::nodeAdded()
{
    // TODO: check why it crashes here!
    endInsertRows();
}

Node *ViewModel::ViewModel::getNode(const QModelIndex &index) const
{
    return static_cast<Node *>(index.internalPointer());
}

int ViewModel::ViewModel::getNodeRow(Node *node) const
{
    int row = 0;

    if (node != NULL)
    {
        const Node *parentItem = node->getParent();

        if (parentItem == NULL)
        {
            row = m_dataModel->getProjectIndex(node);
        }
        else
        {
            row = parentItem->getChildIndex(node);
        }
    }

    return row;
}
