import csv
import re

with open('sbdb_query_results.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    sbdb_query_dict = {}
    for row in csv_reader:
        catalog_num = ''
        nickname = ''
        common_name = ''
        full_name = row['full_name'].strip()
        # set discovery name to the value inside parentheses
        match = re.search('\((.*?)\)', full_name)
        if match:
            discovery_name = match.group(1)
            print('discovery_name: ', discovery_name)
        # if the full name starts with a number, not a parenthesis, get the common name
        if full_name[0].isdigit():
            # grab the string before the first parenthesis
            match = re.search(r'^(.*?)\(', full_name)
            if match:
                common_name = match.group(1)
                cn = common_name.split()
                catalog_num = cn[0]
                if len(cn)== 2:
                    nickname = cn[1]
        sbdb_query_dict_values = [full_name, common_name, catalog_num, nickname]
        sbdb_query_dict.update({discovery_name: sbdb_query_dict_values})

with open('asteroid_name_reference.csv', 'w', newline='') as csvfile:
    fieldnames = ['discovery name', 'full name', 'common name', 'catalog number', 'nickname']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for key, values in sbdb_query_dict.items():
        row = dict(zip(fieldnames, [key] + values))
        writer.writerow(row)