#include "NewProjectDialog.h"
#include "ui_NewProjectDialog.h"

NewProjectDialog::NewProjectDialog(QWidget *parent)
    : QDialog(parent),
      ui(new Ui::NewProjectDialog),
      m_projectName(),
      m_projectDescription()
{
    ui->setupUi(this);
}

NewProjectDialog::~NewProjectDialog()
{
    delete ui;
}

QString NewProjectDialog::getProjectName() const
{
    return m_projectName;
}

QString NewProjectDialog::getProjectDescription() const
{
    return m_projectDescription;
}

void NewProjectDialog::accept()
{
    m_projectName = ui->name_lineEdit->text();
    m_projectDescription = ui->description_plainTextEdit->toPlainText();

    QDialog::accept();
}
