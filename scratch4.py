import csv
from collections import OrderedDict

myDict = OrderedDict([('a', 1), ('b',2),  ('c', 3), ('d', 4),  ('e', 5), ('f', 6)])
print (type(myDict))
print (myDict)
print (type(dict(myDict)))
j = dict(myDict)
for key in j:
    print (key)
print (j)
with open("frequencies.csv", "w") as outfile:
    csvwriter = csv.DictWriter(outfile, fieldnames= myDict)
    csvwriter.writeheader()
    csvwriter.writerow(dict(myDict))
