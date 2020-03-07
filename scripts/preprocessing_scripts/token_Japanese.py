#Performing sentence splitting for all the files in the Input folder
import os
import sys
import rdflib
import nltk
from rdflib import Graph,term,Literal,XSD
from rdflib.namespace import RDFS,RDF, FOAF, NamespaceManager
import string
import codecs
import nagisa
data=sys.argv[1]
for filename in os.listdir('Files/Inputja/'):
	nif=rdflib.Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
	count=0
	#Perform the operation for given input arguments	
	for filename in os.listdir('Files/Inputja/'):
		if (count < int(data)):	
			g=Graph()
			graph2=rdflib.Graph()
			graph2.parse('Files/Inputja/'+filename,format='nt')
			name=filename.split(".")[0]
			s=graph2.serialize(format="nt")
			for s,p,o in graph2:
				if type(o)==rdflib.term.Literal and nif.isString in p:
					sentences = nagisa.tagging(codecs.encode(str(o), encoding='utf-8', errors='replace'))
					sentence=list(sentences.words)
					for i in sentence:
						try:
							BI=o.index(i)
							EI=o.index(i)+len(i)
							g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),RDF.type,nif.Word])
							g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.beginIndex,rdflib.term.Literal(str(BI))])
							g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.endIndex,	rdflib.term.Literal(str(EI))])
							g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.anchorOf,rdflib.term.Literal(i)])
							g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.referenceContext,rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=context")])  
						except:
							pass
			g.bind("nif",nif)        
			g.serialize(destination='Files/Tokens/'+filename,format="turtle")
			count=count+1
print("Your Output is stored in Tokens Folder")
