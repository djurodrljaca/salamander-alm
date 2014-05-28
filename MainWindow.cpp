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
#include "Database/IntegerField.h"
#include "Database/NodeRecord.h"
#include "View/ViewModel.h"
#include <QtCore/QtDebug>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    m_dataModel()
{
    ui->setupUi(this);
    connect(ui->action_Quit, SIGNAL(triggered()), this, SLOT(close()));
    connect(ui->connect_pushButton, SIGNAL(clicked()), this, SLOT(connectButtonPushed()));
    connect(ui->add_pushButton, SIGNAL(clicked()), this, SLOT(addButtonPushed()));
    connect(ui->get_pushButton, SIGNAL(clicked()), this, SLOT(getButtonPushed()));
}

MainWindow::~MainWindow()
{
    m_dataModel.stop();
    delete ui;
}

void MainWindow::connectButtonPushed()
{
    bool success = m_dataModel.start();
    qDebug() << "Data model started:" << success;

    if (success)
    {
        success = m_dataModel.load();
        qDebug() << "Data model loaded:" << success;

        if (success)
        {
            ViewModel::ViewModel *viewModel = new ViewModel::ViewModel(&m_dataModel, this);
            ui->view_treeView->setModel(viewModel);
        }
    }
}

void MainWindow::addButtonPushed()
{
//    if (m_database.isConnected())
//    {
//        using namespace Database;
//        NodeRecord node(IntegerField(), IntegerField(), NodeType_Project);
//        IntegerField id;

//        bool success = m_database.addNode(node, &id);
//        qDebug() << "MainWindow::addButtonPushed:" << success << id;

//        if (success)
//        {
//            node.setParent(id);

//            success = m_database.addNode(node, &id);
//            qDebug() << "MainWindow::addButtonPushed:" << success << id;
//        }
//    }
}

void MainWindow::getButtonPushed()
{
//    if (m_database.isConnected())
//    {
//        using namespace Database;

//        bool success = false;
//        const IntegerField id(1);

//        const NodeRecord node = m_database.getNode(id, &success);
//        qDebug() << "MainWindow::getButtonPushed:" << success << id << node;

//        const IntegerField parent1;
//        const QList<NodeRecord> nodeList1 = m_database.getNodes(parent1, &success);

//        foreach (const NodeRecord nodeItem, nodeList1)
//        {
//            qDebug() << "MainWindow::getButtonPushed:" << success << nodeItem;
//        }

//        const IntegerField parent2 = id;
//        const QList<NodeRecord> nodeList2 = m_database.getNodes(parent2, &success);

//        foreach (const NodeRecord nodeItem, nodeList2)
//        {
//            qDebug() << "MainWindow::getButtonPushed:" << success << nodeItem;
//        }
//    }
}
