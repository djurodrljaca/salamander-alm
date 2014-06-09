#include "NewNodeDialog.h"
#include "ui_NewNodeDialog.h"

NewNodeDialog::NewNodeDialog(QWidget *parent)
    : QDialog(parent),
      ui(new Ui::NewNodeDialog)
{
    ui->setupUi(this);

    QStringList typeList;
    typeList << Database::convertNodeTypeToString(Database::NodeType_Project)
             << Database::convertNodeTypeToString(Database::NodeType_Requirement);

    ui->type_comboBox->insertItems(0, typeList);
}

NewNodeDialog::~NewNodeDialog()
{
    delete ui;
}

Database::NodeType NewNodeDialog::getType() const
{
    const QString typeText = ui->type_comboBox->currentText();
    return Database::convertStringToNodeType(typeText);
}

QString NewNodeDialog::getProjectName() const
{
    return ui->name_lineEdit->text();
}

QString NewNodeDialog::getProjectDescription() const
{
    return ui->description_plainTextEdit->toPlainText();
}
