#Performing Part-of-speech tagging on all files in the Context folder
import rdflib
import nltk
from rdflib import Graph,term,Literal,XSD
from rdflib.namespace import RDFS,RDF, FOAF, NamespaceManager
import string
import os
import sys
import codecs

def main(data,lang,assign):
	print("NLTK code trigerred")
	def spans(txt):
		txt = txt.replace('"', ' ')
		tokens=nltk.word_tokenize(str(txt),language=''+assign+'')
		offset = 0
		for i in range(len(tokens)):
			offset = txt.index(tokens[i], offset)
			yield tokens[i], offset, offset+len(tokens[i])
			offset += len(tokens[i])
		
	nif=rdflib.Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
	track=0
	for filename in os.listdir('Files/Input'+lang+'/'):
		if(track < int(data)):
			name=filename.split(".")[0]
			graph2=rdflib.Graph()
			graph2.parse("Files/Input"+lang+"/"+filename,format='nt')
			g=Graph()
			for s,p,o in graph2:
				if type(o)==rdflib.term.Literal and nif.isString in p:
					sentences = nltk.sent_tokenize(o,language=''+assign+'')
					for i in range(len(sentences)):
						try:
							BII=o.find(sentences[i])
							for token in spans(sentences[i]):
								assert token[0]==sentences[i][token[1]:token[2]]
								BI=BII+token[1]
								EI=BII+token[2]
								if token[0] not in string.punctuation:
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),RDF.type,nif.Word])
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.beginIndex,rdflib.term.Literal(str(BI))])
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.endIndex,rdflib.term.Literal(str(EI))])
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.anchorOf,rdflib.term.Literal(token[0])])
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.referenceContext,rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=context")])       
						except:
							pass
                               
			g.bind("nif",nif)        
			g.serialize(destination="Files/Tokens/"+filename,format="turtle")
			track=track+1
	print("Please Check the Tokens folder for output files")
if __name__ == "__main__":
    main(data,lang,assign)