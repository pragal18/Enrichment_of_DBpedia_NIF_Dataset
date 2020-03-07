Enrichment of DBpedia NIF Dataset
Enrichment of DBpedia NIF Dataset is a compilation of Bash and Python3 scripts that enables to perform various Natural Language
Processing tasks on wikipedia on normal off-the-shelf hardware (e.g., a quad-core CPU, 8 GB of main memory, and 250 GB hard disk 
storage). 

STEP 1:
Download the "nif_context_<language>.ttl" file from https://wiki.dbpedia.org/downloads-2016-10 . Languages supported by this project are 
English, French, German, Spanish and Japanese. So make sure you download the nif-context for any one of these languages. 	

Download nif_text_links_<language>.ttl from the https://wiki.dbpedia.org/ and run the separate_scripts.sh pointing the path of  	
downloaded location of nif_text_links. It creates a CSV file with all links,surface forms and their Part of Speech. This is a           
mandatory step for performing link enrichment task.

STEP 2:
Run the 'separate_scripts.sh' by giving an argument -p followed by the path to the location of "nif_context_<language>.ttl" in your 
system. This is a preprocessing step to perform various Natural Language Processing tasks on individual articles. 

Positional argument:
	-p PATH,
		Specify the location to downloaded nif-context file. 
Optional argument:
	-s Search,
		Specify the file or subset of files that needs to be extracted from nif-context file
Example 
./separate_scripts.sh -p F:/Master_thesis/nif_context_de.ttl (Extracts all the Wikipedia articles in German language and stores in 
Files/Inputde folder)
./separate_scripts.sh -p F:/Master_thesis/nif_context_en.ttl -s St (Extracts all articles that starts with "St" in English Language and 
stores in Files/Inputen folder)
./separate_scripts.sh -p F:/Master_thesis/nif_context_es.ttl -s 5 (Extracts the article 5 in Spanish Language and stores in 
Files/Inputes folder)
./separate_scripts.sh -p F:/Master_thesis/nif_text_links_fr.ttl (Creates a CSV file with all the surfaceforms-Links-POS and store in 
Files/LinkDataset.csv for French Language) 

STEP 3:
Perform various NLP tasks by running 'runme.sh' with the following arguments :
1) Language (-l) - "en" for english, "fr" for French, "de" for German, "ja" for Japanese, "es" for spanish
		 Default language is English if the language parameter is not specified. 
		 Even if you have your own text file, store it under this location and all the tasks could be performed.
2) NLP task (-t) - "SEN" for sentence splitting
	      	   "TOK" for Tokenisation
	           "POS" for Part of speech tagging
	           "ADL" for enrichment of additional links
3) Instance size (-n) - specify the number of wikipedia articles the operation should be performed on.
4) Search(-s) - Article name specify a particular article name for which the operation has to be performed.
5) Tool name(-e)- "NLTK" for Using Natural Language Tool Kit package from Python3 , "TTB" for using TextBlob , "SIO" for using Spacy IO 
                   and "PAT" for Pattern. Default is NLTK is none of it is specified.	
		   
REQUIREMENTS
python>=3.4
NLTK >= 3.0
SPACY>=2.0
rdflib>=4.0
numpy>=1.16.3 
TextBlob>=0.15.2
Pattern >=3.6

USAGE
usage: ./runme.sh [-l LANGUAGE] [-n NUMBER OF FILES TO BE PROCESSED] [-t NLP TASK] [-e NAME OF TOOL] [-s SEARCH]

Perform various NLP Tasks on Wikipedia.
Positional arguments:
     -t  Task,            
     			  We are able to perform 4 NLP tasks here over selected set of wikipedia articles or all the articles in 5       
                          different languages namely 
			  Sentence splitting (SEN), 
			  Tokenization(TOK), 
			  Part of speeching(POS) and 
			  Link Enrichment(ADL).
     -n  Number,          
     			  Specify a number of articles to perform the tasks on. 
  
Optional arguments:
     -s SEARCH,            
                          Enter the name of an article that you would like to perform the NLP task on. You have the option to specify -t 
			  ALL to have all NLP tasks performed for that article. There is no need to mention -n in this case.
     -e TOOL,              
    			  Natural Language ToolKit (NLTK)
			  SPACYIO (SIO)
			  TextBlob (TTB)
			  Pattern(PAT)
                          (default: NLTK)
    -l LANGUAGE, 
                          English(en), German(de), Spanish(es), French(fr) and Japanese(ja) (default: en)

Examples
./runme.sh -t SEN -n 100 (Performs Sentence splitting on 100 english articles via NLTK)  
./runme.sh -t ALL -s Apollos (Performs all 4 NLP tasks for the article Apollos)
./runme.sh -t TOK -n 100 -l de -e SIO (Perform Tokenisation on 100 German articles via Spacy IO)

PROCESSING 
	Download nif_context_en.ttl from the https://wiki.dbpedia.org/ and run the separate_scripts.sh with path as an argument to the 	 
	downloaded location of nif_context. This separates the nif_context_en to RDF triples of individual articles and stores them in 	
	Files/Inputen. If you download nif_context_fr.ttl then output gets stored in Files/Inputfr. Similarly Spanish nif_context_es.ttl 
	gets stored in Files/Inputes and Files/Inputde for German. 
	
	Download nif_text_links_en.ttl from the https://wiki.dbpedia.org/ and run the separate_scripts.sh pointing the path to  	
	downloaded location of nif_text_links. It creates a CSV file with all links,surface forms and their Part of Speech This is a     
	mandatory step for performing link enrichment task. You can terminate the execution of this script at anytime, more the records 
	better the resultset you are expected to get. This CSV file will contain duplicate records. So after this kindly run 
	python final_scripts/LinkDataset_remove_duplicates.py in order to get rid of the duplicate records in CSV file.
	
OUTPUT
	Results of sentence-splitting task gets stored in Files/Sentence folder in RDF triples.
	Results of Tokenization task gets stored in Files/Tokens in RDF triples.
	Results of Part of speech tasks gets stored in the Files/POS in RDF triples on the same name as the article.
	Results of Link Enrichment task gets stored in Files/Links in RDF format.
	Results of Search tasks gets stored on Files/Search with name of the article followed by task in RDF format.	

MORE EXAMPLES

New@DESKTOP-1UH44PA ~
$ ./run.sh -n 5 -t "TOK" -p "GEN"
Please check the Tokens folder for output files

New@DESKTOP-1UH44PA ~
$ ./run.sh -n 5 -t "TOK" -p "GEN" -l "JA"
Please check the Tokens folder for output files