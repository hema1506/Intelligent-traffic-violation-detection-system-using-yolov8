import csv

with open('violations.csv', 'r') as f:
    reader = csv.reader(f)
    rows = list(reader)
    total_violations = len(rows) - 1  # minus header
    no_helmet = 0
    triple_riding = 0
    for row in rows[1:]:
        if "No Helmet" in row[2]:
            no_helmet += 1
        elif "Triple Riding" in row[2]:
            triple_riding += 1

print("Total violations detected: {}".format(total_violations))
print("No Helmet violations: {}".format(no_helmet))
print("Triple Riding violations: {}".format(triple_riding))
