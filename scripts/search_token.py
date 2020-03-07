#performing tokenization for all the files in a folder
import os
from rdflib import Graph,term,Literal,XSD
from rdflib.namespace import RDFS,RDF, FOAF, NamespaceManager
import string
import sys
import rdflib
import spacy
def main(lang,filename):
	nlp = spacy.load('en_core_web_sm')
	nif=rdflib.Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
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
					BII=o.encode(sys.stdout.encoding, errors='replace').index(i.text.encode(sys.stdout.encoding, errors='replace'))
					EII=o.encode(sys.stdout.encoding, errors='replace').index(i.text.encode(sys.stdout.encoding, errors='replace'))+len(i.text.encode(sys.stdout.encoding, errors='replace'))
					inner=nlp(i.text.encode().decode('utf-8'))
					offset=0
					for ing in inner:
						offset = i.text.encode().decode('utf-8').index(ing.text.encode().decode('utf-8'),offset)
						BI= offset+ BII
						EI=BI +len(ing.text.encode().decode('utf-8'))
						offset=offset+len(ing.text.encode().decode('utf-8'))
						if ing.text.encode().decode('utf-8') not in string.punctuation:
							g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),RDF.type,nif.Word])
							g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.beginIndex,rdflib.term.Literal(str(BI))])
							g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.endIndex,	rdflib.term.Literal(str(EI))])
							g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.anchorOf,rdflib.term.Literal(ing.text.encode().decode('utf-8'))])
							g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.referenceContext,rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=context")])  
				except:
					pass
	g.bind("nif",nif)        
	g.serialize(destination='Files/Search/'+filename+'-token.ttl',format="turtle")
	print("Your Output is stored in Search Folder")

if __name__ == "__main__":
    main(lang,filename)