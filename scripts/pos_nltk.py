#Performing Part-of-speech tagging on all files in the Context folder
import rdflib
import nltk
from rdflib import Graph,term,Literal,XSD
from rdflib.namespace import RDFS,RDF, FOAF, NamespaceManager
import string
import os
import sys
import codecs
import pandas as pd

data = [
['NNP','Noun','ProperNoun'], 
['NN','Noun','Noun'], 
['VB',	'Verb',	'Verb'],
['DT','DET','Determiner'], 
['JJS',	'ADJ',	'Adjective'],
['JJR',	'ADJ',	'Adjective'],
['NN',	'Noun',	'Noun'],
['NNS',	'Noun',	'NounPlural'],
['JJ',	'ADJ',	 'Adjective'],
['IN',	'preposition',	'Preposition'],
['NNS','Noun','NounPlural'],
['VBD',	'Verb',	'VerbPastTense'],
['VBG',	'Verb',	'Verb'],
['VBP',	'Verb',	'Verb'],
['VBN',	'Verb',	'VerbPastParticiple'],
['VBZ',	'Verb',	'VerbSingularPresent'],
['RB',	'ADV',	'Adverb'],
['RBR',	'ADV',	'Adverb'],
['RBS',	'ADV',	'Adverb'],
['WDT',	'DET',	'Wh-Determiner'],
['PDT',	'DET',	'Predeterminer'],
['WP',	'Pronoun',	'wh-Pronoun'],
['PRP',	'Pronoun',	'PersonalPronoun'],
['CC',	'CON',	'Conjunction']
 ]
df = pd.DataFrame(data, columns = ['POS','SF','FF'])  

def main(data,lang,assign):
	nif=rdflib.Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
	track=0
	print("NLTK pos code trigerred")
	def spans(txt):
		txt = txt.replace('"', ' ')
		tokens=nltk.word_tokenize(str(txt),language=''+assign+'')
		tagged=nltk.pos_tag(tokens,lang=''+lang+'')		
		offset = 0
		check=0		
		for i in range(len(tokens)):
			codecs.encode(str(tokens[i].encode().decode('utf-8')), encoding='utf-8', errors='replace')
			offset = txt.index(tokens[i], offset)
			yield tokens[i], offset, offset+len(tokens[i]) , tagged[i][1]
			offset += len(tokens[i])
			check=check+1
  
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
						count=0
						try:
							BII=o.find(sentences[i])
							for token in spans(sentences[i]):
								assert token[0]==sentences[i][token[1]:token[2]]
								BI=BII+token[1]
								EI=BII+token[2]
								value=df['SF'][df['POS']==token[3]]
								for val in value:
									hell="http://purl.org/olia/olia.owl#"+val
								fullvalue=df['FF'][df['POS']==token[3]]	
								for jval in  fullvalue:
									hello="http://purl.org/olia/olia.owl#"+jval
							
								if token[0] not in string.punctuation:
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),RDF.type,nif.Word])
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.beginIndex,rdflib.term.Literal(str(BI))])
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.endIndex,rdflib.term.Literal(str(EI))])
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.anchorOf,rdflib.term.Literal(token[0])])
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.referenceContext,rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=context")])       
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.oliaLink,rdflib.term.URIRef("http://purl.org/olia/penn.owl#"+token[3])])
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.oliaCategory,term.URIRef(hello)])                         
									g.add([rdflib.term.URIRef("http://dbpedia.org/resource/"+name+"?dbpv=2016-10&nif=word_offset_"+str(BI)+"_"+str(EI)),nif.oliaCategory,term.URIRef(hell)])
								count=count+1
						except:
							pass
                               
			g.bind("nif",nif)        
			g.serialize(destination="Files/POS/"+filename,format="turtle")
			track=track+1
	print("Please Check the POS folder for output files")

if __name__ == "__main__":
    main(data,lang,assign)