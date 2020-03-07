import rdflib
import nltk
import xlrd
import csv 
import codecs
import string
import re
import nltk
from nltk.corpus import stopwords
from rdflib import Graph,term,Literal,XSD
from rdflib.namespace import RDFS,RDF, FOAF, NamespaceManager

def main(lang,name):
	graph2=rdflib.Graph()
	g=rdflib.Graph()
	nif=rdflib.Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
	itsrdf= rdflib.Namespace("http://www.w3.org/2005/11/its/rdf#") 
	dbp=rdflib.Namespace("http://dbpedia.org/resource/")
	graph2.parse("Files/Input"+lang+"/"+name+".ttl",format='nt')
	counter=0
	i=0
	stop = set(stopwords.words('english'))
	for s,p,o in graph2:
		if type(o)==rdflib.term.Literal and nif.isString in p:
			tokens=nltk.word_tokenize(o)
			pos=nltk.pos_tag(tokens)
			count=len(nltk.word_tokenize(o))-3
			while i<count:
				save3=""
				save2=""
				save=""
				a=tokens[i]

				if tokens[i] not in string.punctuation and tokens[i] not in stop:
					b=tokens[i+1]
					c=tokens[i+2]
					string2=a+' '+b+' '+c
					string1=a+' '+b
					csvreader = csv.reader(codecs.open('Files/LinkDataset'+lang+'.csv','r',encoding='mac_roman',errors='ignore')) 
					fields = next(csvreader)
					for row in csvreader:
						if row[0].split(" ")[0].lower() == a.lower() and row[2].split(" ")[0]== pos[i][1] :
							if row[0].lower() == string2.lower():
								save3=row[1]
								ind=re.search(string2.lower(), o.lower())
								counter=ind.start()
								g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=phrase_offset_"+str(counter)+"_"+str(counter+len(string2))),RDF.type,nif.Phrase])
								g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=phrase_offset_"+str(counter)+"_"+str(counter+len(string2))),nif.referenceContext,rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=context")])
								g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=phrase_offset_"+str(counter)+"_"+str(counter+len(string2))),nif.beginIndex,rdflib.term.Literal(str(counter))])
								g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=phrase_offset_"+str(counter)+"_"+str(counter+len(string2))),nif.endIndex,rdflib.term.Literal(str(counter+len(string2)))])
								g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=phrase_offset_"+str(counter)+"_"+str(counter+len(string2))),nif.anchorOf,rdflib.term.Literal(string2)])                  
								g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=phrase_offset_"+str(counter)+"_"+str(counter+len(string2))),itsrdf.taIdentRef,rdflib.term.URIRef("http://dbpedia.org/resource/"+row[0].replace(" ","_"))])
								i=i+2
								counter=counter+len(b)+len(c)-1							
								break
							elif row[0].lower()==string1.lower():
								ind=re.search(string1.lower(), o.lower())
								keyword2=row[0]
								save2=row[1]
								i=i+1
								break
							
							elif row[0].lower()==a.lower() and save=="":
								ind=re.search(a.lower(), o.lower())
								keyword=row[0]
								save=row[1]
                            
					if save2 and save3=="" and ind.start()>=counter:
						counter=ind.start()
						g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=phrase_offset_"+str(counter)+"_"+str(counter+len(string1))),RDF.type,nif.Phrase])
						g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=phrase_offset_"+str(counter)+"_"+str(counter+len(string1))),nif.referenceContext,rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=context")])
						g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=phrase_offset_"+str(counter)+"_"+str(counter+len(string1))),nif.beginIndex,rdflib.term.Literal(str(counter))])
						g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=phrase_offset_"+str(counter)+"_"+str(counter+len(string1))),nif.endIndex,rdflib.term.Literal(str(counter+len(string1)))])
						g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=phrase_offset_"+str(counter)+"_"+str(counter+len(string1))),nif.anchorOf,rdflib.term.Literal(string1)])                  
						g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=phrase_offset_"+str(counter)+"_"+str(counter+len(string1))),itsrdf.taIdentRef,rdflib.term.URIRef("http://dbpedia.org/resource/"+keyword2.replace(" ","_"))])
						counter=counter+len(b)-1						
                    
					elif save and save3=="" and ind.start()>=counter:
						counter=ind.start()
						g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(counter)+"_"+str(counter+len(a))),RDF.type,nif.Word])
						g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(counter)+"_"+str(counter+len(a))),nif.referenceContext,rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=context")])
						g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(counter)+"_"+str(counter+len(a))),nif.beginIndex,rdflib.term.Literal(str(counter))])
						g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(counter)+"_"+str(counter+len(a))),nif.endIndex,rdflib.term.Literal(str(counter+len(a)))])
						g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(counter)+"_"+str(counter+len(a))),nif.anchorOf,rdflib.term.Literal(a)])
						g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(counter)+"_"+str(counter+len(a))),itsrdf.taIdentRef,rdflib.term.URIRef("http://dbpedia.org/resource/"+keyword)])
					counter+=len(a)-1

				
				else:
					counter=counter-1
				counter+=1
				i=i+1
            
	g.bind("nif",nif)
	g.bind("itsrdf",itsrdf)
	g.bind("dbp",dbp)
	g.serialize(destination="Files/Search/"+name+"-links.ttl",format="turtle")
	print("Your output is stored on the Search folder")   

if __name__ == "__main__":
    main(lang,filename)