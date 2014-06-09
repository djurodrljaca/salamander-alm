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
#include "NewNodeDialog.h"
#include <QtCore/QtDebug>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent),
      ui(new Ui::MainWindow),
      m_treeViewModel(this)
{
    ui->setupUi(this);

    ui->view_treeView->setModel(&m_treeViewModel);
    ui->view_treeView->header()->hide();

    connect(ui->view_treeView, SIGNAL(clicked(QModelIndex)),
            this, SLOT(loadNode(QModelIndex)));
    connect(ui->action_Quit, SIGNAL(triggered()),
            this, SLOT(close()));
    connect(ui->connect_pushButton, SIGNAL(clicked()),
            this, SLOT(connectToModel()));
    connect(ui->addNode_pushButton, SIGNAL(clicked()),
            this, SLOT(addNode()));
    connect(ui->saveNode_pushButton, SIGNAL(clicked()),
            this, SLOT(saveNode()));
    connect(ui->revertNode_pushButton, SIGNAL(clicked()),
            this, SLOT(revertNode()));
    connect(ui->removeNode_pushButton, SIGNAL(clicked()),
            this, SLOT(removeNode()));
}

MainWindow::~MainWindow()
{
    m_treeViewModel.stop();
    delete ui;
}

void MainWindow::loadNode(QModelIndex modelIndex)
{
    DataModel::Node node;

    if (modelIndex.isValid())
    {
        node = m_treeViewModel.getNode(modelIndex);
    }

    if (node.isValid())
    {
        ui->nodeType_lineEdit->setText(Database::convertNodeTypeToString(node.getType()));

        ui->nodeName_lineEdit->setText(node.getName());
        ui->nodeName_lineEdit->setEnabled(true);
        ui->nodeName_lineEdit->setReadOnly(false);

        ui->nodeDescription_plainTextEdit->setPlainText(node.getDescription());
        ui->nodeDescription_plainTextEdit->setEnabled(true);
        ui->nodeDescription_plainTextEdit->setReadOnly(false);

        ui->removeNode_pushButton->setEnabled(true);
        ui->saveNode_pushButton->setEnabled(true);
        ui->revertNode_pushButton->setEnabled(true);
    }
    else
    {
        clearNodeView();
    }
}

void MainWindow::connectToModel()
{
    if (m_treeViewModel.isStarted())
    {
        m_treeViewModel.stop();
        ui->connect_pushButton->setText("Connect");
    }
    else
    {
        bool success = m_treeViewModel.start();

        if (success)
        {
            success = m_treeViewModel.load();
        }

        if (success)
        {
            ui->connect_pushButton->setText("Disconnect");
        }
        else
        {
            m_treeViewModel.stop();
        }
    }

    clearNodeView();
}

void MainWindow::addNode()
{
    NewNodeDialog dialog;
    int result = dialog.exec();

    if (result == QDialog::Accepted)
    {
        const QModelIndex modelIndex = getSelectedNodeModelIndex();
        const Database::NodeType nodeType = dialog.getType();
        const QString name = dialog.getProjectName();
        const QString description = dialog.getProjectDescription();

        if (modelIndex.isValid())
        {
            m_treeViewModel.addItem(modelIndex, nodeType, name, description);
        }
        else
        {
            m_treeViewModel.addItem(QModelIndex(), nodeType, name, description);
        }
    }
}

void MainWindow::saveNode()
{
    const QModelIndex modelIndex = getSelectedNodeModelIndex();

    if (modelIndex.isValid())
    {
        DataModel::Node node = m_treeViewModel.getNode(modelIndex);

        if (node.isValid())
        {
            // Check if any of the node properties changed
            const QString name = ui->nodeName_lineEdit->text();

            if (name != node.getName())
            {
                node.setName(name);
            }

            const QString description = ui->nodeDescription_plainTextEdit->toPlainText();

            if (description != node.getDescription())
            {
                node.setDescription(description);
            }

            // Updated changed properties
            if (node.hasChanged())
            {
                m_treeViewModel.updateNode(node);
            }
        }
    }
}

void MainWindow::revertNode()
{
    const QModelIndex modelIndex = getSelectedNodeModelIndex();

    if (modelIndex.isValid())
    {
        DataModel::Node node = m_treeViewModel.getNode(modelIndex);

        if (node.isValid())
        {
            ui->nodeName_lineEdit->setText(node.getName());
            ui->nodeDescription_plainTextEdit->setPlainText(node.getDescription());
        }
    }
}

void MainWindow::removeNode()
{
    const QModelIndex modelIndex = getSelectedNodeModelIndex();

    if (modelIndex.isValid())
    {
        DataModel::Node node = m_treeViewModel.getNode(modelIndex);

        if (node.isValid())
        {
            // Deactivate node
            node.setActive(false);

            if (node.hasChanged())
            {
                if (m_treeViewModel.updateNode(node))
                {
                    clearNodeView();
                }
            }
        }
    }
}

void MainWindow::clearNodeView()
{
    ui->nodeType_lineEdit->clear();

    ui->nodeName_lineEdit->clear();
    ui->nodeName_lineEdit->setEnabled(false);
    ui->nodeName_lineEdit->setReadOnly(true);

    ui->nodeDescription_plainTextEdit->clear();
    ui->nodeDescription_plainTextEdit->setEnabled(false);
    ui->nodeDescription_plainTextEdit->setReadOnly(true);

    ui->removeNode_pushButton->setEnabled(false);
    ui->saveNode_pushButton->setEnabled(false);
    ui->revertNode_pushButton->setEnabled(false);
}

QModelIndex MainWindow::getSelectedNodeModelIndex() const
{
    QModelIndex modelIndex;
    QItemSelectionModel *selectionModel = ui->view_treeView->selectionModel();

    if (selectionModel != NULL)
    {
        QModelIndexList modelIndexList = selectionModel->selectedIndexes();

        if (!modelIndexList.isEmpty())
        {
            modelIndex = modelIndexList.at(0);
        }
    }

    return modelIndex;
}
