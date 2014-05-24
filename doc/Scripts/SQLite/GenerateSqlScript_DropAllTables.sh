#!/bin/sh

sqlTables=$( < "./Tables/CreateTableOrder.txt" )
outputFile=DropAllTables.sqlite

if [ -f $outputFile ];
then
	rm $outputFile
fi

for table in $sqlTables
do
	echo "DROP TABLE ${table};" >> $outputFile
done