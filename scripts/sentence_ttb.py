#Performing sentence splitting for all the files in the Input folder
import os
import sys
import rdflib
from rdflib import Graph,term,Literal,XSD
from rdflib.namespace import RDFS,RDF, FOAF, NamespaceManager
import textblob
from textblob import TextBlob
import string
import codecs
def main(data,lang):
	print("Sentence splitting via TextBlob")
	nif=rdflib.Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
	count=0
	i=0
	for filename in os.listdir('Files/Input'+lang+'/'):
		if (count < int(data)):
			graph2=rdflib.Graph()
			graph2.parse('Files/Input'+lang+'/'+filename,format='nt')
			g=Graph()
			name=filename.split(".")[0]
			s=graph2.serialize(format="nt")
			for s,p,o in graph2:
				if type(o)==rdflib.term.Literal and nif.isString in p:
					codecs.encode(str(o), encoding='utf-8', errors='replace')
					wiki=TextBlob(str(o))
					for i in wiki.sentences:
						codecs.encode(str(i), encoding='utf-8', errors='replace')
						try:
							BI=str(o).index(str(i))
							EI=o.index(str(i))+len(str(i))
							g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=sentence_offset_"+str(BI)+"_"+str(EI)),RDF.type,nif.Sentence])
							g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=sentence_offset_"+str(BI)+"_"+str(EI)),nif.beginIndex,rdflib.term.Literal(str(BI))])
							g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=sentence_offset_"+str(BI)+"_"+str(EI)),nif.endIndex,rdflib.term.Literal(str(EI))])
							g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=sentence_offset_"+str(BI)+"_"+str(EI)),nif.anchorOf,rdflib.term.Literal(str(i))])
							g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=sentence_offset_"+str(BI)+"_"+str(EI)),nif.referenceContext,rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=context")])     
						except:
							pass
			g.bind("nif",nif)        
			g.serialize(destination='Files/Sentence/'+filename,format="turtle")
			count=count+1
	print("Your Output is stored in Sentence Folder")
	
if __name__ == "__main__":
    main(data,lang)