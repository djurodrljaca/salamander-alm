#ifndef NEWPROJECTDIALOG_H
#define NEWPROJECTDIALOG_H

#include "Database/NodeType.h"
#include <QDialog>

namespace Ui {
class NewNodeDialog;
}

class NewNodeDialog : public QDialog
{
    Q_OBJECT

public:
    explicit NewNodeDialog(QWidget *parent = 0);
    ~NewNodeDialog();

    Database::NodeType getType() const;
    QString getProjectName() const;
    QString getProjectDescription() const;

private:
    Ui::NewNodeDialog *ui;
};

#endif // NEWPROJECTDIALOG_H
