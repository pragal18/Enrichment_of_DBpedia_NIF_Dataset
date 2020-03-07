#Performing sentence splitting for all the files in the Input folder
import os
import sys
import rdflib
from rdflib import Graph,term,Literal,XSD
from rdflib.namespace import RDFS,RDF, FOAF, NamespaceManager
import spacy

def main(lang,filename):
	nif=rdflib.Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
	count=0
	nlp = spacy.load('en_core_web_sm')
	if lang != "en" :
		nlp = spacy.load(''+lang+'_core_news_sm')    
	graph2=rdflib.Graph()
	graph2.parse('Files/Input'+lang+'/'+filename+'.ttl',format='nt')
	g=Graph()
	name=filename.split(".")[0]
	s=graph2.serialize(format="nt")
	for s,p,o in graph2:
		if type(o)==rdflib.term.Literal and nif.isString in p:
			sentences = nlp(o.encode().decode('utf-8'))
			for i in sentences.sents:
				try:
					BI=o.encode(sys.stdout.encoding, errors='replace').index(i.text.encode(sys.stdout.encoding, errors='replace'))
					EI=BI+len(i.text.encode(sys.stdout.encoding, errors='replace'))
					g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=sentence_offset_"+str(BI)+"_"+str(EI)),RDF.type,nif.Sentence])
					g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=sentence_offset_"+str(BI)+"_"+str(EI)),nif.beginIndex,rdflib.term.Literal(str(BI))])
					g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=sentence_offset_"+str(BI)+"_"+str(EI)),nif.endIndex,rdflib.term.Literal(str(EI))])
					g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=sentence_offset_"+str(BI)+"_"+str(EI)),nif.anchorOf,rdflib.term.Literal(i.text)])
					g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=sentence_offset_"+str(BI)+"_"+str(EI)),nif.referenceContext,rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=context")])    
				except:
					pass
	g.bind("nif",nif)        
	g.serialize(destination='Files/Search/'+filename+'-sentence.ttl',format="turtle")		
	print("Your Output is stored in Search Folder")

if __name__ == "__main__":
    main(lang,filename)