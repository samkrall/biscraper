import pandas as pd
import json
import os
from zipfile import ZipFile
import shutil
import ast
import openpyxl

filepath = r"\\ad.sjm.com\cvd\CVD Departments\Market Research Core Team\Sam\NMD Project\\".replace('\\', '/')
directory_path = os.path.dirname(filepath)
os.chdir(directory_path)
print("New Directory:", os.getcwd())

filename = 'NMD OEM Model.pbit'
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
    print(relationship)
    Relationship = []
    Relationship.append(relationship['fromTable']+'.'+relationship['fromColumn'])
    Relationship.append(relationship['toTable']+'.'+relationship['toColumn'])
    try:
        Relationship.append(relationship['fromCardinality'])
    except:
        Relationship.append('Many-to-One')
    try:
        Relationship.append(relationship['crossFilteringBehavior'])
    except:
        Relationship.append('Single')
    
    Relationship_list.append(Relationship)
relationship_list_df = pd.DataFrame(Relationship_list, columns = ['From', 'To', 'Cardinality', 'CrossFiltering'])
relationship_list_df['Cardinality'] = relationship_list_df['Cardinality'].apply(lambda x: 'One-to-One' if x == 'one' else x)

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
            Measure.append(measure['name'])
            Measure.append(','.join(measure['expression'][1:]).replace(',', '').strip())
            joined_string = ','.join(measure['expression'])
            Measure_list.append(Measure)
    
    except:
            continue

 
        
measure_list_df = pd.DataFrame(Measure_list, columns = ['Table', 'MeasureName', 'Expression'])

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
shutil.rmtree(filepath+'/temp')
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    # Write each dataframe to a different worksheet
    source_list_df.to_excel(writer, sheet_name='Sources', index=False)
    relationship_list_df.to_excel(writer, sheet_name='Relationships', index=False)
    column_list_df.to_excel(writer, sheet_name='Columns', index=False)
    measure_list_df.to_excel(writer, sheet_name='Measures', index=False)
    visual_df.to_excel(writer, sheet_name='Visuals', index=False)
