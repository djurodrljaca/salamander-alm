/**
 * @file   MainWindow.cpp
 * @author Djuro Drljaca (djurodrljaca@gmail.com)
 * @date   2014-5-24
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

#include "MainWindow.h"
#include "ui_MainWindow.h"
#include "Database/Integer.h"
#include "Database/Node.h"
#include <QtCore/QtDebug>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    m_database()
{
    ui->setupUi(this);
    connect(ui->action_Quit, SIGNAL(triggered()), this, SLOT(close()));
    connect(ui->connect_pushButton, SIGNAL(clicked()), this, SLOT(connectButtonPushed()));
    connect(ui->add_pushButton, SIGNAL(clicked()), this, SLOT(addButtonPushed()));
    connect(ui->get_pushButton, SIGNAL(clicked()), this, SLOT(getButtonPushed()));
}

MainWindow::~MainWindow()
{
    m_database.disconnect();
    delete ui;
}

void MainWindow::connectButtonPushed()
{
    bool success = m_database.connect();
    qDebug() << "Database opened:" << success;

    if (success)
    {
        success = m_database.validate();
        qDebug() << "Database valid:" << success;
    }

    if (!success)
    {
        success = m_database.create();
        qDebug() << "Database reinitialized:" << success;
    }
}

void MainWindow::addButtonPushed()
{
    if (m_database.isConnected())
    {
        using namespace Database;
        Node node(Integer(), Integer(), NodeType_Project);
        Integer id;

        bool success = m_database.addNode(node, &id);
        qDebug() << "MainWindow::addButtonPushed:" << success << id;

        if (success)
        {
            node.setParent(id);

            success = m_database.addNode(node, &id);
            qDebug() << "MainWindow::addButtonPushed:" << success << id;
        }
    }
}

void MainWindow::getButtonPushed()
{
    if (m_database.isConnected())
    {
        using namespace Database;

        bool success = false;
        const Integer id(1);

        const Node node = m_database.getNode(id, &success);
        qDebug() << "MainWindow::getButtonPushed:" << success << id << node;

        const Integer parent1;
        const QList<Node> nodeList1 = m_database.getNodes(parent1, &success);

        foreach (const Node nodeItem, nodeList1)
        {
            qDebug() << "MainWindow::getButtonPushed:" << success << nodeItem;
        }

        const Integer parent2 = id;
        const QList<Node> nodeList2 = m_database.getNodes(parent2, &success);

        foreach (const Node nodeItem, nodeList2)
        {
            qDebug() << "MainWindow::getButtonPushed:" << success << nodeItem;
        }
    }
}
