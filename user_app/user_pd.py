import pandas as pd

with open('filter.py', 'r') as f:
    general = f.readlines()
    file_name, text = general[0], general[1:]

text = [line.replace('\n', '').strip().replace('  ', ' ') for line in text]
separates = ['>=', '<=', '!=', '>', '<', '=']
print(f"{text}\n")
filters = []
for line in text:
    for sep in separates:
        if len(line.split(sep)) != 1:
        	item = [obj.strip().replace(' ', '_') if index==0 else obj.strip() for index, obj in enumerate(line.split(sep))]
        	# 91  , 92, 93, 46
        	separated_items = item[1].replace(', ', ',').split(',')
        	if len(separated_items) > 1:
        		for one in separated_items:
        			filters.append([item[0], sep.replace('=', '==') if len(sep)==1 else sep, int(one.strip()) if one.strip().isdigit() else one])
        	else:
        		item.insert(1, sep.replace('=', '==') if len(sep)==1 else sep)
        		if item[2].isdigit():
        			item[2] = int(item[2])
        		filters.append(item)
        	break

for i in filters:
    print(i)


# Then we get DataFrame from .csv or .xlsx
file_format = file_name.split('.')[1]
if 'csv' in str(file_format):
	df = pd.read_csv(file_name.replace('\n', ''))
elif 'xlsx' in str(file_format):
	df = pd.read_excel(file_name)
else:
	print(f"We don't know this format .{file_format}")

# Replace spaces in column names
df.columns = [x.replace(' ', '_') for x in df.columns]

for item in filters:
	if isinstance(item[2], int):
		df = df.query(f"{item[0]}{item[1]}{item[2]}")
	else:
		df = df.query(f"{item[0]}{item[1]}'{item[2]}'")

print(f'\n{df}')
