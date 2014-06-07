#include "NewNodeDialog.h"
#include "ui_NewNodeDialog.h"

NewNodeDialog::NewNodeDialog(QWidget *parent)
    : QDialog(parent),
      ui(new Ui::NewNodeDialog)
{
    ui->setupUi(this);
}

NewNodeDialog::~NewNodeDialog()
{
    delete ui;
}

QString NewNodeDialog::getProjectName() const
{
    return ui->name_lineEdit->text();
}

QString NewNodeDialog::getProjectDescription() const
{
    return ui->description_plainTextEdit->toPlainText();
}
