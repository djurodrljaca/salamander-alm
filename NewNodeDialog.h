#ifndef NEWPROJECTDIALOG_H
#define NEWPROJECTDIALOG_H

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

    QString getProjectName() const;
    QString getProjectDescription() const;

private:
    Ui::NewNodeDialog *ui;
};

#endif // NEWPROJECTDIALOG_H
