/**
 * @file   DataModel.h
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-06-06
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

#ifndef DATAMODEL_DATAMODEL_H
#define DATAMODEL_DATAMODEL_H

#include "Database/SqliteDatabase.h"
#include "DataModel/DataModelItem.h"
#include "DataModel/Node.h"
#include <QtCore/QList>
#include <QtCore/QMap>

namespace DataModel
{
class DataModel
{
public:
    DataModel();
    ~DataModel();

    bool start();
    void stop();

    bool load(const Database::IntegerField &requestedRevisionId = Database::IntegerField());

    bool login(const QString &username, const QString &password);

    int getRootItemCount() const;
    DataModelItem * getRootItem(const int index) const;
    int getRootItemIndex(DataModelItem *item) const;

    DataModelItem * getItem(const Database::IntegerField &id) const;
    bool addItem(const Database::IntegerField &parentId,
                 const Database::NodeType nodeType,
                 const QString &name,
                 const QString &description);

    Database::IntegerField getItemId(DataModelItem *item) const;
    Node getNode(const Database::IntegerField &id) const;
    bool updateNode(const Node &node);

private:
    bool loadRootDataModelItemsFromDatabase(const Database::IntegerField &revisionId);
    bool loadDataModelItemFromDatabase(const Database::NodeRecord &nodeRecord,
                                       const Database::IntegerField &revisionId,
                                       DataModelItem *parent,
                                       DataModelItem *node);
    bool loadDataModelItemChildrenFromDatabase(const Database::IntegerField &revisionId,
                                               DataModelItem *parent);

    Database::SqliteDatabase m_database;
    QList<DataModelItem *> m_itemList;
    QMap<qlonglong, DataModelItem *> m_itemMap;
    Database::IntegerField m_revisionId;
    Database::IntegerField m_userId;
};
}

#endif // DATAMODEL_DATAMODEL_H
