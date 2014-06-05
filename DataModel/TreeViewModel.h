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

#include "Database/SqliteDatabase.h"
#include "DataModel/Node.h"
#include <QtCore/QList>
#include <QtCore/QAbstractItemModel>

namespace DataModel
{
class TreeViewModel : public QAbstractItemModel
{
    Q_OBJECT

public:
    TreeViewModel(QObject *parent = NULL);
    ~TreeViewModel();

    bool start();
    void stop();

    bool load();

    bool addProject(const QString &name, const QString description);
    //bool addNode(const QModelIndex &parent, const Node &node);

    QVariant data(const QModelIndex &index, int role) const;
    Qt::ItemFlags flags(const QModelIndex &index) const;
    QModelIndex index(int row, int column, const QModelIndex &parent = QModelIndex()) const;
    QModelIndex parent(const QModelIndex &index) const;
    int rowCount(const QModelIndex &parent = QModelIndex()) const;
    int columnCount(const QModelIndex &parent = QModelIndex()) const;

private:
    int getProjectCount() const;
    Node * getProject(const int index) const;
    int getProjectIndex(Node *projectNode) const;

    Node *getNode(const QModelIndex &index) const;
    int getNodeRow(Node *node) const;

    bool loadNodeFromDatabase(const Database::NodeRecord &nodeRecord,
                              Node *parent,
                              Node *node) const;
    bool contains(Node *node) const;

    Database::SqliteDatabase m_database;
    QList<Node *> m_projectList;
};
}

#endif // DATAMODEL_TREEVIEWMODEL_H
