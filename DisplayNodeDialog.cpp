#include "DisplayNodeDialog.h"
#include "ui_DisplayNodeDialog.h"

DisplayNodeDialog::DisplayNodeDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::DisplayNodeDialog)
{
    ui->setupUi(this);
}

DisplayNodeDialog::~DisplayNodeDialog()
{
    delete ui;
}

QString DisplayNodeDialog::getProjectName() const
{
    return ui->name_lineEdit->text();
}

void DisplayNodeDialog::setProjectName(const QString &projectName)
{
    ui->name_lineEdit->setText(projectName);
}

QString DisplayNodeDialog::getProjectDescription() const
{
    return ui->description_plainTextEdit->toPlainText();
}

void DisplayNodeDialog::setProjectDescription(const QString &projectDescription)
{
    ui->description_plainTextEdit->setPlainText(projectDescription);
}
