#ifndef NEWPROJECTDIALOG_H
#define NEWPROJECTDIALOG_H

#include <QDialog>

namespace Ui {
class NewProjectDialog;
}

class NewProjectDialog : public QDialog
{
    Q_OBJECT

public:
    explicit NewProjectDialog(QWidget *parent = 0);
    ~NewProjectDialog();

    QString getProjectName() const;
    QString getProjectDescription() const;

public slots:
    void accept();

private:
    Ui::NewProjectDialog *ui;
    QString m_projectName;
    QString m_projectDescription;
};

#endif // NEWPROJECTDIALOG_H
