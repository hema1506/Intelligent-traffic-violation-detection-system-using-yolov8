import csv

f = open('viol file.ations/violation_details.csv', 'r')
r = csv.DictReader(f)
rows = list(r)
print('Total rows:', len(rows))

empty_conf = [row for row in rows if not row.get('Confidence') or not row.get('Confidence').strip()]
print('Rows with empty confidence:', len(empty_conf))

if empty_conf:
    print('First few empty rows:')
    for row in empty_conf[:5]:
        print(row)

f.close()
