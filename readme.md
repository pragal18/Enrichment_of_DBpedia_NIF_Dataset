# Enrichment of DBpedia NIF Dataset

[![Build Status](https://github.com/pragal18/Enrichment_of_DBpedia_NIF_Dataset/blob/master/readme.md)](https://alfresco.fit.cvut.cz/share/proxy/alfresco/api/node/content/workspace/SpacesStore/9bc256c6-4881-4990-a49f-6ced5f9222ef)

Enrichment of DBpedia NIF Dataset is a compilation of Python3 and Shell scripts that enables to perform various Natural Language Processing tasks on wikipedia on normal off-the-shelf hardware (e.g., a quad-core CPU, 8 GB of main memory, and 250 GB hard disk 
storage). 

# REQUIREMENTS
- Python3
- Rdflib >= 4.0 &nbsp; &nbsp; https://pypi.org/project/rdflib/
- Numpy >=1.16.3 &nbsp; &nbsp;  https://pypi.org/project/numpy/ 
- Pandas >= 1.0 &nbsp;  &nbsp; https://pypi.org/project/pandas/
- NLTK >= 3.0 &nbsp;  &nbsp; https://pypi.org/project/nltk/
- Spacy >=2.0 &nbsp; &nbsp; https://pypi.org/project/spacy/
- TextBlob >=0.15.2  &nbsp;  &nbsp;  https://pypi.org/project/textblob/
- Pattern >=3.6  &nbsp;  &nbsp; https://pypi.org/project/Pattern/
- StanfordPOSTagger >= 3.9.0  &nbsp; &nbsp; https://nlp.stanford.edu/software/tagger.shtml
- Konoha,Nagisa (for Processing Japanese language) &nbsp; &nbsp; https://pypi.org/project/konoha/  &nbsp; &nbsp; https://pypi.org/project/nagisa/

# Processing steps
  ## STEP 1: 
Download the NIF Context file from https://wiki.dbpedia.org/downloads-2016-10 in the ttl format. Languages supported in this project are :
 - English (nif_context_en.ttl), 
 - French (nif_context_fr.ttl), 
 - German (nif_context_de.ttl), 
 - Spanish (nif_context_es.ttl) and 
 - Japanese (nif_context_ja.ttl). \
Download the language(s) that is required for you. Extract them after downloading. A minimal version of these files are created and are stored on NIF_Dataset_Minimal_Version at home directory of this project.
 
Similarly download NIF Text Links file from the https://wiki.dbpedia.org/downloads-2016-10 in TTL format for any of the above mentioned languages. Extract it after downloading. NIF Text Links file is required only if you would like to perform the 'enhancement of links' NLP task. The minimal version of these datasets are stored at 'NIF_Dataset_Minimal_Version/' directory. 


 ## STEP 2:
 Clone this git repository on your local system. 
 'separate_scripts.sh' and 'run.sh' need to be executed in order to perform pre-preocessing tasks and NLP tasks respectively. In order to execute the shell scripts, run the following 4 commands from the home directory:
 ```sh
sed -i 's/\r//' run.sh
sed -i 's/\r//' separate_scripts.sh 
chmod +x run.sh
chmod +x separate_scripts.sh
```
 ## STEP 3:
Run the 'separate_script.sh' with an argument -p specifying the path where **NIF context** file is stored in the system. The result of "Separation of Wikipedia articles" task will be saved in 'Files/Input-language_name' directory. 
 - Positional argument:  
&nbsp; &nbsp; -p PATH,  
&nbsp; &nbsp;  Specify the location to downloaded nif-context file. 
 - Optional argument: \
&nbsp; &nbsp; -s SEARCH, \
&nbsp; &nbsp; Specify the article(s) that needs to be extracted from nif-context file

__Examples__
```sh
./separate_scripts.sh -p F:/Master_thesis/nif_context_de.ttl 
 ```
 Extracts all the articles in German language and stores in Files/Inputde directory
 ```sh
./separate_scripts.sh -p F:/Master_thesis/nif_context_en.ttl -s St
 ```
 Extracts all articles that starts with "St" in English Language and stores in Files/Inputen folder
 ```sh
./separate_scripts.sh -p F:/Master_thesis/nif_context_es.ttl -s Apocopis
```
Extracts the article Apocopis in Spanish Language and stores in Files/Inputes folder

Similarly for performing Links Enhancement NLP task, Run the 'separate_script.sh' again with an argument -p specifying the path where **NIF Text Links** file is stored in the system. The result of "Surface forms analysis" task will be stored in a CSV file saved at 'Files/LinkDataset-languagename_with_duplicates.csv'. 
```sh
./separate_scripts.sh -p F:/Master_thesis/nif_text_links_fr.ttl
```
Creates surface forms CSV file with the surfaceforms-Links-POS for French Language and stores it in  Files/LinkDatasetfr_with_duplicates.csv

This might contain duplicate records. So just to speed up the NLP task, you should run the python script LinkDataset_remove_duplicates.py located at scripts/preprocessing_scripts.
```sh
python scripts/preprocessing_scripts/LinkDataset_remove_duplicates.py
```
Duplicates are removed and result is stored at Files/LinkDataset-languagename.csv


## STEP 4:
Perform Sentence-splitting, Tokenisation, Part-of-speech tagging and Enhance Links by running the script run.sh with the following argument(s) :
- Language - **en** for english, **fr** for French, **de** for German, **ja** for Japanese, **es** for spanish. Default language is English.

- NLP task - **SEN** for sentence splitting, **TOK** for Tokenisation, **POS** for Part of speech tagging, **LINK** for enrichment of additional links

- Instance size - Number of articles for which the NLP task(s) should be performed. Default integer is 1.

- Search - Specify a particular article name for which the NLP Task(s) has to be performed.

- Tool name - **NLTK** for Natural Language Tool Kit package, **TTB** for using TextBlob , **SIO** for using SpacyIO and **PAT** for Pattern. Default is NLTK.	

### USAGE:
```sh
 ./run.sh [ -l LANGUAGE] [ -n INSTANCE SIZE] [ -t NLP TASK] [-e TOOL NAME] [-s SEARCH] 
 ```
**Positional arguments**:
- **-t** &nbsp; &nbsp; NLP TASK,            
Specify SEN, TOK, POS or LINK
- **-n** &nbsp; &nbsp; INSTANCE SIZE ,          
Specify an integer. (Default: 1)
  
**Optional arguments**:
- **-s** &nbsp; &nbsp; SEARCH,            
Specify the name of an article. You have an option to specify -t ALL to have all NLP tasks performed for this article.
- **-e** &nbsp; &nbsp; TOOL,              
Specify NLTK, SIO, TTB or PAT. (Default: NLTK)
- **-l** &nbsp; &nbsp; LANGUAGE, 
Specify en, de, fr, es or ja. (Default: en)

**Examples**
```sh
./run.sh -t SEN -n 100
```
Performs Sentence splitting on 100 English articles through NLTK
```sh
./run.sh -t ALL -s Apollos 
```
Performs all 4 NLP tasks for the article Apollos
```sh
./run.sh -t TOK -n 100 -l de -e TTB
```
Performs Tokenisation on 100 German articles through TextBlob
```sh
./run.sh -t POS -n 10 -l es -e SIO 
```
Performs Part-of-Speech tagging for 10 Spanish articles through SpacyIO
```sh
./run.sh -t LINK -n 10 -l fr -e NLTK
```
Enhances Links for 10 French Articles through NLTK
	
# OUTPUT
Results of sentence-splitting task gets stored in Files/Sentence folder in RDF triples. \
Results of Tokenization task gets stored in Files/Tokens in RDF triples. \
Results of Part of speech tasks gets stored in the Files/POS in RDF triples on the same name as the article. \
Results of Link Enrichment task gets stored in Files/Links in RDF format. \
Results of Search tasks gets stored on Files/Search with name of the article followed by task in RDF format.	
