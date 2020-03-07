import rdflib
import nltk
import xlrd
import csv 
import codecs
import string
import re
import nltk
import os
from nltk.corpus import stopwords
import textblob
from textblob import TextBlob
from rdflib.namespace import RDFS,RDF, FOAF, NamespaceManager

def main(data,lang):
	print("code for TextBlob Links trigerred")
	nif=rdflib.Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
	itsrdf= rdflib.Namespace("http://www.w3.org/2005/11/its/rdf#") 
	dbp=rdflib.Namespace("http://dbpedia.org/resource/")
	total=0
	#Perform the operation for given input arguments	
	for filename in os.listdir('Files/Input'+lang+'/'):
		if (total < int(data)):	
			graph2=rdflib.Graph()
			g=rdflib.Graph()
			graph2.parse("Files/Input"+lang+"/"+filename,format='nt')
			name=filename.split(".")[0]
			counter=0
			i=0
			stop = set(stopwords.words('english'))
			s=graph2.serialize(format="nt")
			for s,p,o in graph2:
				if type(o)==rdflib.term.Literal and nif.isString in p:
					wiki=TextBlob(str(o))
					count=len(wiki.tags)-3
					while i<count:
						save3=""
						save2=""
						save=""
						a=wiki.tags[i][0]
						if wiki.tags[i][0] not in string.punctuation and wiki.tags[i][0] not in stop:
							b=wiki.tags[i+1][0]
							c=wiki.tags[i+2][0]
							string2=a+' '+b+' '+c
							string1=a+' '+b
							csvreader = csv.reader(codecs.open('Files/LinkDataset'+lang+'.csv','r',encoding='mac_roman',errors='ignore')) 
							fields = next(csvreader)
							for row in csvreader:
								if row[0].split(" ")[0].lower() == a.lower() and row[2].split(" ")[0]== wiki.tags[i][1] :
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
										counter=counter+len(b)+len(c)							
										break
									elif row[0].lower()==string1.lower():
										ind=re.search(string1.lower(), o.lower())
										keyword2=row[0]
										save2=row[1]
										i=i+1
										break
							
									elif row[0].lower()==a.lower() and save=="":
										keyword=row[0]
										ind=re.search(a.lower(), o.lower())
										save=row[1]
                            
							if save2 and save3=="" and ind.start()>=counter:
								counter=ind.start()
								g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=phrase_offset_"+str(counter)+"_"+str(counter+len(string1))),RDF.type,nif.Phrase])
								g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=phrase_offset_"+str(counter)+"_"+str(counter+len(string1))),nif.referenceContext,rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=context")])
								g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=phrase_offset_"+str(counter)+"_"+str(counter+len(string1))),nif.beginIndex,rdflib.term.Literal(str(counter))])
								g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=phrase_offset_"+str(counter)+"_"+str(counter+len(string1))),nif.endIndex,rdflib.term.Literal(str(counter+len(string1)))])
								g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=phrase_offset_"+str(counter)+"_"+str(counter+len(string1))),nif.anchorOf,rdflib.term.Literal(string1)])                  
								g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=phrase_offset_"+str(counter)+"_"+str(counter+len(string1))),itsrdf.taIdentRef,rdflib.term.URIRef("http://dbpedia.org/resource/"+keyword2.replace(" ","_"))])
								counter=counter+len(b)							
                    
							elif save and save3=="" and ind.start()>=counter:
								counter=ind.start()
								g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(counter)+"_"+str(counter+len(a))),RDF.type,nif.Word])
								g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(counter)+"_"+str(counter+len(a))),nif.referenceContext,rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=context")])
								g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(counter)+"_"+str(counter+len(a))),nif.beginIndex,rdflib.term.Literal(str(counter))])
								g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(counter)+"_"+str(counter+len(a))),nif.endIndex,rdflib.term.Literal(str(counter+len(a)))])
								g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(counter)+"_"+str(counter+len(a))),nif.anchorOf,rdflib.term.Literal(a)])
								g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(counter)+"_"+str(counter+len(a))),itsrdf.taIdentRef,rdflib.term.URIRef("http://dbpedia.org/resource/"+keyword)])
							counter+=len(a)

						counter+=1
						i=i+1
            
			g.bind("nif",nif) 
			g.bind("itsrdf",itsrdf)
			g.bind("dbp",dbp)		
			g.serialize(destination="Files/Links/"+name+"-links.ttl",format="turtle")
			total=total+1
	print("Your output is stored on the Links folder")   

if __name__ == "__main__":
    main(n,lang)