#!/usr/bin/python 
import  sentence_nltk, sentence_nltk, token_nltk, pos_nltk, sentence_sio, token_sio, pos_sio ,sentence_ttb , token_ttb, pos_ttb, sentence_pat
import search_sentence, search_token, search_pos , pos_nltk_lang , search_link , link_nltk , link_sio , link_ttb
import sys

def getassign():
	if lang=="en":
		return "english"
	elif lang=="fr":
		return "french"
	elif lang=="es":
		return "spanish"
	elif lang=="de":
		return "german"
	else:
		return "english"
	
def exec():
	if tool=="NLTK" or tool=="nltk":
		assign=getassign()
		if task=="SEN" or task=="sen":
			sentence_nltk.main(n,lang,assign)
		elif task=="TOK" or task=="tok":
			token_nltk.main(n,lang,assign)
		elif task=="POS" or task=="pos":
			if lang=="en" or lang=="ja" :
				pos_nltk.main(n,lang,assign)
			else:
				pos_nltk_lang.main(n,lang,assign)
		elif task=="LINK" or task=="link":
			link_nltk.main(n,lang,assign)
		else:
			print("Invalid task")
	elif tool=="SIO" or tool=="sio":
		if task=="SEN" or task=="sen":
			sentence_sio.main(n,lang)
		elif task=="TOK" or task=="tok":
			token_sio.main(n,lang)
		elif task=="POS" or task=="pos":
			pos_sio.main(n,lang)
		elif task=="LINK" or task=="link":
			link_sio.main(n,lang)
		else:
			print("Invalid task")	
	elif tool=="TTB" or tool=="ttb":
		if task=="SEN" or task=="sen":
			sentence_ttb.main(n,lang)
		elif task=="TOK" or task=="tok":
			token_ttb.main(n,lang)
		elif task=="POS" or task=="pos":
			pos_ttb.main(n,lang)
		elif task=="LINK" or task=="link":
			link_ttb.main(n,lang)
		else:
			print("Invalid task")
	elif tool=="PAT" or tool=="pat":
		if task=="SEN" or task=="sen":
			sentence_pat.main(n,lang)
		# elif task=="TOK":
			# token_ttb.main(n,lang)
		# elif task=="POS":
			# pos_ttb.main(n,lang)
		else:
			print("Invalid task for PATTERN library")			
	else:
		print("Invalid tool chosen")

def exec_search():
	if task=="ALL" or task=="all":
		search_sentence.main(lang,search)
		search_token.main(lang,search)
		search_pos.main(lang,search)
		search_link.main(lang,search)
	elif task=="SEN" or task=="sen":
		search_sentence.main(lang,search)
	elif task=="TOK" or task=="tok":
		search_token.main(lang,search)
	elif task=="POS" or task=="pos":
		search_pos.main(lang,search)
	elif task=="LINK" or task=="link" or task=="Link":
		search_link.main(lang,search)
	else:
		print("Invalid task")		

n=sys.argv[1]
task=sys.argv[2]
search=sys.argv[3]
tool=sys.argv[4]
lang=sys.argv[5]

if search == "NA" :
	exec()
else:
	search=search.split(".")[0]
	exec_search()
