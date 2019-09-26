# MockSqlData
This package is to generate mock data based on table definitions.
preserves referential integrity

#set-up
install python,pip
pip install faker,pandas

#Schema Definition 
follow the format in template.json

#run 
format
python loadData.py templateJson testCasesCount
example :
python loadData.py template.json 100
