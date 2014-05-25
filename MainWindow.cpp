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
#include "Database/DataTypes/Integer.h"
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
        using namespace Database::DataTypes;
        Integer id;

        bool success = m_database.addNode(Integer(), Integer(1), &id);
        qDebug() << "MainWindow::addButtonPushed:" << success << id.toString();
    }
}

void MainWindow::getButtonPushed()
{
    if (m_database.isConnected())
    {
        using namespace Database::DataTypes;
        using namespace Database::Tables;

        bool success = false;
        const Integer id(1);
        const Node node = m_database.getNode(id, &success);
        qDebug() << "MainWindow::getButtonPushed:" << success << id.toString() << node.toString();
    }
}
