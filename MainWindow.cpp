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
#include "NewProjectDialog.h"
#include "DisplayNodeDialog.h"
#include <QtCore/QtDebug>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    m_treeViewModel(this)
{
    ui->setupUi(this);

    ui->view_treeView->setModel(&m_treeViewModel);
    ui->view_treeView->header()->hide();

    connect(ui->view_treeView, SIGNAL(doubleClicked(QModelIndex)), this, SLOT(displayNode(QModelIndex)));
    connect(ui->action_Quit, SIGNAL(triggered()), this, SLOT(close()));
    connect(ui->connect_pushButton, SIGNAL(clicked()), this, SLOT(connectButtonPushed()));
    connect(ui->addProject_pushButton, SIGNAL(clicked()), this, SLOT(addProjectButtonPushed()));
}

MainWindow::~MainWindow()
{
    m_treeViewModel.stop();
    delete ui;
}

void MainWindow::displayNode(QModelIndex modelIndex)
{
    const DataModel::Node *node = m_treeViewModel.getNode(modelIndex);

    if (node != NULL)
    {
        DisplayNodeDialog dialog;
        dialog.setProjectName(node->getName());

        // TODO: det description from database
        //node->getDescriptionId()
        //dialog.setProjectDescription();

        dialog.exec();
    }
}

void MainWindow::connectButtonPushed()
{
    bool success = m_treeViewModel.start();
    qDebug() << "Data model started:" << success;

    if (success)
    {
        success = m_treeViewModel.load();
        qDebug() << "Data model loaded:" << success;
    }
}

void MainWindow::addProjectButtonPushed()
{
    NewProjectDialog dialog;

    int result = dialog.exec();

    if (result == QDialog::Accepted)
    {
        const QString name = dialog.getProjectName();
        const QString description = dialog.getProjectDescription();

        bool success = m_treeViewModel.addProject(name, description);
        qDebug() << "MainWindow::addButtonPushed: project added:" << success;
    }

//    QItemSelectionModel *selectionModel = ui->view_treeView->selectionModel();

//    if (selectionModel != NULL)
//    {
//        QModelIndex modelIndex = selectionModel->currentIndex();

//        DataModel::Node node;
//        node.setType(Database::NodeType_Project);

//        bool success = m_treeViewModel.addNode(modelIndex, node);
//        qDebug() << "MainWindow::addButtonPushed: success:" << success;
//    }
}
