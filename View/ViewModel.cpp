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

ViewModel::ViewModel::ViewModel(DataModel::DataModel *dataModel, const int projectIndex, QObject *parent)
    : QAbstractItemModel(parent),
      m_dataModel(dataModel),
      m_projectNode(NULL)
{
    if (m_dataModel != NULL)
    {
        m_projectNode = m_dataModel->getProject(projectIndex);
    }
}

ViewModel::ViewModel::~ViewModel()
{
    // TODO: should the data model be deleted?
}

QVariant ViewModel::ViewModel::data(const QModelIndex &index, int role) const
{
    QVariant dataValue;

    if (index.isValid() &&
        (role == Qt::DisplayRole))
    {
        Node *item = static_cast<Node *>(index.internalPointer());

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

QVariant ViewModel::ViewModel::headerData(int section, Qt::Orientation orientation, int role) const
{
    if (orientation == Qt::Horizontal && role == Qt::DisplayRole)
    {
        return QVariant("Header");
    }

    return QVariant();
}

QModelIndex ViewModel::ViewModel::index(int row, int column, const QModelIndex &parent) const
{
    QModelIndex modelIndex;

    if (hasIndex(row, column, parent))
    {
        Node *parentItem = NULL;

        if (!parent.isValid())
        {
            parentItem = m_projectNode;
        }
        else
        {
            parentItem = static_cast<Node *>(parent.internalPointer());
        }

        if (parentItem != NULL)
        {
            Node *childItem = parentItem->getChild(row);

            if (childItem != NULL)
            {
                modelIndex = createIndex(row, column, childItem);
            }
        }
    }

    return modelIndex;
}

QModelIndex ViewModel::ViewModel::parent(const QModelIndex &index) const
{
    QModelIndex modelIndex;

    if (index.isValid())
    {
        Node *childItem = static_cast<Node *>(index.internalPointer());

        if (childItem != NULL)
        {
            Node *parentItem = childItem->getParent();

            if (parentItem != m_projectNode)
            {
                int row = 0;

                if (parentItem != NULL)
                {
                    Node *grandparentItem = parentItem->getParent();

                    if (grandparentItem != NULL)
                    {
                        row = grandparentItem->getChildIndex(parentItem);
                    }
                }

                modelIndex = createIndex(row, 0, parentItem);
            }
        }
    }

    return modelIndex;
}

int ViewModel::ViewModel::rowCount(const QModelIndex &parent) const
{
    Node *parentItem = NULL;
    int count = 0;

    const int column = parent.column();

    if (column <= 0)
    {
        if (!parent.isValid())
        {
            parentItem = m_projectNode;
        }
        else
        {
            parentItem = static_cast<Node *>(parent.internalPointer());
        }

        if (parentItem != NULL)
        {
            count = parentItem->getChildCount();
        }
    }

    return count;
}

int ViewModel::ViewModel::columnCount(const QModelIndex &) const
{
    return 1;
}
