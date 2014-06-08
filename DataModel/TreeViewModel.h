/**
 * @file   TreeTreeViewModel.h
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

#ifndef DATAMODEL_TREEVIEWMODEL_H
#define DATAMODEL_TREEVIEWMODEL_H

#include "DataModel/DataModel.h"
#include "DataModel/Node.h"
#include <QtCore/QAbstractItemModel>

namespace DataModel
{
class TreeViewModel : public QAbstractItemModel
{
    Q_OBJECT

public:
    TreeViewModel(QObject *parent = NULL);
    ~TreeViewModel();

    bool isStarted() const;
    bool start();
    void stop();

    bool load();

    bool login(const QString &username, const QString &password);

    bool addItem(const QModelIndex &index,
                 const Database::NodeType nodeType,
                 const QString &name,
                 const QString &description);
    bool updateNode(const Node &node);
    Node getNode(const QModelIndex &index) const;

    QVariant data(const QModelIndex &index, int role) const;
    Qt::ItemFlags flags(const QModelIndex &index) const;
    QModelIndex index(int row, int column, const QModelIndex &parent = QModelIndex()) const;
    QModelIndex parent(const QModelIndex &index) const;
    int rowCount(const QModelIndex &parent = QModelIndex()) const;
    int columnCount(const QModelIndex &parent = QModelIndex()) const;

private:
    QModelIndex parent(DataModelItem *item) const;
    DataModelItem *getDataModelItem(const QModelIndex &index) const;
    int getItemRow(DataModelItem *item) const;

    DataModel m_dataModel;
};
}

#endif // DATAMODEL_TREEVIEWMODEL_H
