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

    QString getProjectName() const;
    void setProjectName(const QString &projectName);

    QString getProjectDescription() const;
    void setProjectDescription(const QString &projectDescription);

    bool getRemoveNode() const;

private:
    Ui::DisplayNodeDialog *ui;
};

#endif // DISPLAYNODEDIALOG_H
