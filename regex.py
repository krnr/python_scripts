import re

data = open('regex_sum_193468.txt')
result, sum = [], 0
for line in data:
    found = re.findall('[0-9]+', line)
    if len(found) > 0: result = result + found

print sum(int(result))