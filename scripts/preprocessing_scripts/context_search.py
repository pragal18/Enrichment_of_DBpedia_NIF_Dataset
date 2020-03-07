#Separating contents of context file downloaded from NIF DBpedia 
import os
import sys
previousSubject=None
path=sys.argv[1]
search=sys.argv[2]
search=search.split(".")[0]
print(search.title())
check=path[len(path)-6:len(path)-4]
if check=="en":
	i=29
else:	
	i=32
with open(path,encoding="utf-8") as openfileobject:
	for line in openfileobject:
		if 'dbpedia.org/resource/'+search.title()+'' in line:
			s=line.find('?')
			thisSubject=line[i:s]
			if previousSubject==thisSubject:
				f.write(line);
			else:
				try:  
					f=open("Files/Input"+check+"/"+thisSubject+".ttl",'a',encoding="utf-8")
					f.write(line);
				except:
					pass  
				
