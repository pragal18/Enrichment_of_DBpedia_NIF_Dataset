#performing tokenization for all the files in a folder
import os
from rdflib import Graph,term,Literal,XSD
from rdflib.namespace import RDFS,RDF, FOAF, NamespaceManager
import string
import sys
import rdflib
import spacy
import re
import pandas as pd
data = [
['PROPN','Noun','ProperNoun'], 
['NOUN','Noun','Noun'], 
['VERB','Verb',	'Verb'],
['DET','DET','Determiner'], 
['ADP','preposition','Preposition'],
['CCONJ','CON','Conjunction'],
['ADJ',	'ADJ','Adjective'],
['ADV',	'ADV','Adverb'],
['PRON','Pronoun','PersonalPronoun'],
['SPACE','Space','TabSpace'],
['NUM','NUM','Number'],
['AUX','AUX','Auxiliary']
]
df = pd.DataFrame(data, columns = ['POS','SF','FF']) 

def main(data,lang):
	track=0
	nif=rdflib.Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
	print("code for spacyIO pos trigerred")
	if lang != "en" :
		nlp = spacy.load(''+lang+'_core_news_sm')
	else:	
		nlp = spacy.load('en_core_web_sm')	
		
	for filename in os.listdir('Files/Input'+lang+'/'):
		if(track < int(data)):	
			graph2=rdflib.Graph()
			graph2.parse('Files/Input'+lang+'/'+filename,format='nt')
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
								value=df['SF'][df['POS']==ing.pos_]
								for val in value:
									hell="http://purl.org/olia/olia.owl#"+ val
								fullvalue=df['FF'][df['POS']==ing.pos_]	
								for jval in  fullvalue:
									hellos="http://purl.org/olia/olia.owl#"+ jval
								if ing.text.encode().decode('utf-8') not in string.punctuation:
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),RDF.type,nif.Word])
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.beginIndex,rdflib.term.Literal(str(BI))])
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.endIndex,	rdflib.term.Literal(str(EI))])
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.anchorOf,rdflib.term.Literal(ing.text.encode().decode('utf-8'))])
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.referenceContext,rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=context")])
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.oliaLink,term.URIRef("http://purl.org/olia/penn.owl#"+ ing.tag_)])                         								
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.oliaCategory,term.URIRef(hellos)])                         
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.oliaCategory,term.URIRef(hell)])						
						except:
							pass
			g.bind("nif",nif)        
			g.serialize(destination='Files/POS/'+filename,format="turtle")
			track=track+1
	print("Your Output is stored in POS Folder via spacyio")

if __name__ == "__main__":
    main(data,lang)