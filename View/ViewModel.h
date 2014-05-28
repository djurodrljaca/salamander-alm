/**
 * @file   ViewModel.h
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

#ifndef VIEW_VIEWMODEL_H
#define VIEW_VIEWMODEL_H

#include "DataModel/DataModel.h"
#include <QAbstractItemModel>

namespace ViewModel
{
class ViewModel : public QAbstractItemModel
{
    Q_OBJECT

public:
    ViewModel(DataModel::DataModel *dataModel, const int projectIndex, QObject *parent = 0);
    ~ViewModel();

    QVariant data(const QModelIndex &index, int role) const;
    Qt::ItemFlags flags(const QModelIndex &index) const;
    QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const;
    QModelIndex index(int row, int column, const QModelIndex &parent = QModelIndex()) const;
    QModelIndex parent(const QModelIndex &index) const;
    int rowCount(const QModelIndex &parent = QModelIndex()) const;
    int columnCount(const QModelIndex &parent = QModelIndex()) const;

private:
    DataModel::DataModel *m_dataModel;
    DataModel::Node *m_projectNode;
};
}

#endif // VIEW_VIEWMODEL_H
