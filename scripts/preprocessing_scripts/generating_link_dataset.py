import csv
import os
import sys
import nltk
import rdflib
from rdflib import Graph
from nltk.tag.stanford import StanfordPOSTagger
path=sys.argv[1]
lang=path[len(path)-6:len(path)-4]
if lang=="en":
	link="https://dbpedia.org/resource/"
else:
	link="https://"+lang+".dbpedia.org/resource/"
fields=	['Surface-Form', 'Link', 'Part-of-Speech'] 
fp=open('Files/LinkDataset'+lang+'_with_duplicates.csv','w',encoding="utf-8",newline='')
with open(path,encoding="utf-8") as openfileobject:
		a = csv.writer(fp, delimiter=',')
		a.writerow(fields)
		for line in openfileobject: 
			if 'http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#anchorOf' in line:
				f=line.index('"')+1
				s=line.index('"', line.index('"') + 1)
				sf=line[f:s]
				word=sf.replace(" ","_").capitalize()
				tokens=nltk.word_tokenize(sf)
				tag=nltk.pos_tag(tokens)
				lists=[]
				for i in tag:
					lists.append(i[1])
					combined =' '.join(lists)
				data = [[str(sf),link+word,combined]]
				a.writerows(data)
	

			
			
			
				
			
					