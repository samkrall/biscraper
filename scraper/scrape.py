import pandas as pd
import json
import os
from zipfile import ZipFile
import shutil
import ast

filepath = 'C:/Users/samdk/Downloads/'
filename = 'sss.pbit'
dms_path = 'DataModelSchema'
layout_path = 'Report/Layout'
f = ZipFile(filepath+filename)
f.extractall(filepath+'temp')

dms = json.loads(
    open(f'{filepath}/temp/DataModelSchema', 'r', encoding='utf-16 le').read())

layout = json.loads(
    open(f'{filepath}temp/Report/Layout', 'r', encoding='utf-16 le').read())

# tables and mcode into a dataframe
source_list = []
for table in dms['model']['tables']:
    source = []
    source.append(table['partitions'][0]['name'])
    source.append('\n'.join(table['partitions'][0]['source']['expression']))
    source_list.append(source)
source_list_df = pd.DataFrame(source_list, columns = ['Table', 'Query'])

# relationships into a dataframe
Relationship_list = []
for relationship in dms['model']['relationships']:
    Relationship = []
    Relationship.append(relationship['fromTable']+'.'+relationship['fromColumn'] + ' to ' +relationship['toTable']+'.'+relationship['toColumn'])
    Relationship_list.append(Relationship)
relationship_list_df = pd.DataFrame(Relationship_list, columns = ['Relationship'])

# columns into a dataframe
Column_list = []
for table in dms['model']['tables']:
    for column in table['columns']:
        Column = []
        Column.append(table['name'])
        Column.append(column['name'])
        Column_list.append(Column)

column_list_df = pd.DataFrame(Column_list, columns = ['Table','Column'])

# measures into a dataframe
Measure_list = []
for table in dms['model']['tables']:
    try:
        for measure in table['measures']:
            Measure = []
            Measure.append(table['name'])
            Measure.append(measure['name']+': ' + measure['expression'])
            Measure_list.append(Measure)
    except:
        continue
measure_list_df = pd.DataFrame(Measure_list, columns = ['Table', 'Measure'])

visual_list = []
visual_ignore_list = ['actionButton', 'basicShape', 'image', 'textbox']
for page in layout['sections']:
    for visual in page['visualContainers']:
        newly_parsed = json.loads(visual['config'])
        if newly_parsed['singleVisual']['visualType'] in visual_ignore_list:
            continue
        else:
            for k, v in newly_parsed['singleVisual']['projections'].items():
                for i in v:
                    visual = []
                    visual.append(page['displayName'])
                    visual.append(newly_parsed['singleVisual']['visualType'])
                    visual.append(i['queryRef'])
                    visual_list.append(visual)

visual_df = pd.DataFrame(visual_list, columns = ['Page', 'Visual', 'Table.Column'])
print(visual_df.shape)

#remove temp folder when finished
#shutil.rmtree(filepath+'/temp')
