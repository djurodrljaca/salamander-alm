#ifndef DISPLAYNODEDIALOG_H
#define DISPLAYNODEDIALOG_H

#include <QDialog>

namespace Ui {
class DisplayNodeDialog;
}

class DisplayNodeDialog : public QDialog
{
    Q_OBJECT

public:
    explicit DisplayNodeDialog(QWidget *parent = 0);
    ~DisplayNodeDialog();

    void setProjectName(const QString &projectName);
    void setProjectDescription(const QString &projectDescription);

private:
    Ui::DisplayNodeDialog *ui;
    QString m_projectName;
    QString m_projectDescription;
};

#endif // DISPLAYNODEDIALOG_H
