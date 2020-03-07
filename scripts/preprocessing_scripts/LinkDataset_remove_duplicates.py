import csv
import codecs
print("Please enter the language for which the duplicates has to be removed (en or fr or de or es or ja) : ")
lang=input()
with codecs.open('Files/LinkDataset'+lang+'_with_duplicates.csv','r',encoding='mac_roman',errors='ignore') as in_file, codecs.open('Files/LinkDataset'+lang+'.csv','w',encoding='mac_roman',errors='ignore') as out_file:
    seen = set() # set for fast O(1) amortized lookup
    for line in in_file:
        if line in seen: continue # skip duplicate
        seen.add(line)
        out_file.write(line)
						