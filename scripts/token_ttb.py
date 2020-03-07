#performing tokenization for all the files in a folder
import os
import nltk
from rdflib import Graph,term,Literal,XSD
from rdflib.namespace import RDFS,RDF, FOAF, NamespaceManager
import string
import sys
import rdflib
import textblob
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
import codecs
def main(data,lang):
	track=0
	nif=rdflib.Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
	print("TextBlob code trigerred")
	def spans(txt):
		hello=TextBlob(txt)
		offset = 0
		tokens=hello.words
		for token in hello.words:
			offset = txt.find(token, offset)
			yield token, offset, offset+len(token)
			offset += len(token)
        
	for filename in os.listdir('Files/Input'+lang+'/'):
		if(track < int(data)):
			graph2=rdflib.Graph()
			graph2.parse('Files/Input'+lang+'/'+filename,format='nt')
			g=Graph()
			name=filename.split(".")[0]
			s=graph2.serialize(format="nt")
			for s,p,o in graph2:
				if type(o)==rdflib.term.Literal and nif.isString in p:
					codecs.encode(str(o), encoding='utf-8', errors='replace')
					wiki = TextBlob(str(o))
					for i in range(len(wiki.sentences)):
						codecs.encode(str(i), encoding='utf-8', errors='replace')
						count=0
						try:
							BII=str(o).index(str(wiki.sentences[i]))
							for token in spans(str(wiki.sentences[i])):
								assert token[0]==str(wiki.sentences[i])[token[1]:token[2]]
								BI=BII+token[1]
								EI=BII+token[2]
								if token[0] not in string.punctuation:
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),RDF.type,nif.Word])
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.beginIndex,rdflib.term.Literal(str(BI))])
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.endIndex,	rdflib.term.Literal(str(EI))])
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.anchorOf,rdflib.term.Literal(token[0])])
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.referenceContext,rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=context")])       
						except:
							pass       
			g.bind("nif",nif)        
			g.serialize(destination='Files/Tokens/'+filename,format="turtle")
			track=track+1
	print("Please check the Tokens folder for output files")

if __name__ == "__main__":
    main(data,lang)