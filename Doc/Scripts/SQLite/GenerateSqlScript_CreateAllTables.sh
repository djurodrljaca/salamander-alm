#!/bin/sh

sqlTables=$( < "./Tables/CreateTableOrder.txt" )
outputFile=CreateAllTables.sqlite

if [ -f $outputFile ];
then
	rm $outputFile
fi

for table in $sqlTables
do
	cat "./Tables/CreateTable_${table}.sqlite" >> $outputFile
	echo "" >> $outputFile
	echo "" >> $outputFile
done