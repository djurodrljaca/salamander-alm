#include "DisplayNodeDialog.h"
#include "ui_DisplayNodeDialog.h"

DisplayNodeDialog::DisplayNodeDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::DisplayNodeDialog),
    m_projectName(),
    m_projectDescription()
{
    ui->setupUi(this);
}

DisplayNodeDialog::~DisplayNodeDialog()
{
    delete ui;
}

void DisplayNodeDialog::setProjectName(const QString &projectName)
{
    m_projectName = projectName;

    ui->name_lineEdit->setText(projectName);
}

void DisplayNodeDialog::setProjectDescription(const QString &projectDescription)
{
    m_projectDescription = projectDescription;

    ui->description_plainTextEdit->setPlainText(projectDescription);
}
