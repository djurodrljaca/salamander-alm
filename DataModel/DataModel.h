/**
 * @file   DataModel.h
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

#ifndef DATAMODEL_DATAMODEL_H
#define DATAMODEL_DATAMODEL_H

#include "Database/SqliteDatabase.h"
#include "DataModel/Node.h"
#include <QtCore/QList>

namespace DataModel
{
class DataModel
{
public:
    DataModel();

    bool start();
    void stop();

    bool load();

private:
    bool loadNodeFromDatabase(const Database::NodeRecord &nodeRecord,
                              Node *node,
                              Node *parent = NULL) const;

    Database::SqliteDatabase m_database;
    QList<Node> m_nodeList;
};
}

#endif // DATAMODEL_DATAMODEL_H
