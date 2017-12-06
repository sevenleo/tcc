#import nltk
import sys
import os
import wikipedia
import pickle
import re
from nltk.corpus import stopwords
from unicodedata import normalize
from gensim.models import Word2Vec



def logs(titulo,texto="",texto2="",content=""):
	titulo = str(titulo).upper()
	texto = str(texto)
	texto2 = str(texto2)
	log = "\n\n"
	log = "\n\n--------------------------------------------\n"
	log = log + titulo.upper()
	log = log + " :\t"+texto
	if texto2 != "":
		log = log + "\n"+texto2+""
	log = log + "\n--------------------------------------------\n"
	print (log)
	print (content)

def tokenize(frase):
	tokens=[]
	lang = "portuguese"
	for word in nltk.word_tokenize(frase, lang):
			#tokens.append(word.decode("utf-8"))
			tokens.append(word)
	return tokens

def sentenizer(text):
	lang = "portuguese"
	sentences = nltk.sent_tokenize(text,language=lang)
	print("Number of senteces:  "+str(len(sentences)))
	return sentences

def cleantext(text):
	if type(text) == str:
		logs("Clean","string")
		text = normalize('NFKD', text).encode('ASCII','ignore').decode('ASCII')
		text = text.replace("\n",". ") ##TROCAR POR EXPRESSAO REGULAR, POIS É MAIS RAPIDO
		text = re.sub("[^a-zA-Z1-9,.ç: ]+", "", text)
		text = re.sub(r"[']", '', text)
		text = re.sub(r"ˈ", '', text)
		text = re.sub("[.]+", ".", text)
		return text
	else:
		string = ''
		for sent in text:
			for word in sent:
				if word.lower() in stopw:
					continue
				word = normalize('NFKD', word).encode('ASCII','ignore').decode('ASCII')
				word = word.replace("\n",". ")
				word = re.sub("[^a-zA-Z1-9]+", "", word)
				word = re.sub(r"[']", '', word)
				word = re.sub(r"ˈ", '', word)
				string += word
				string += " "
			string += ". "
		return string

def search(word,lang="pt"):
	_type = 'string'
	folder = 'SEARCH'
	name = word
	try:
		text = loadfromfile(folder,name,_type)
		return text
	except:
		import wikipedia
		wikipedia.set_lang(lang)
		results = wikipedia.search(word)
		page = wikipedia.page(results[0])
		#text = wikipedia.summary(newword)
		text = page.content
		saveinfile(text,folder,name,_type)
		return text

def saveinfile(obj,_folder,_name,_type):
	if not os.path.exists(_folder):
		os.makedirs(_folder)
	savefilename = _folder+'/'+_name+'.'+_type+'.objb'
	logs("SAVE FILE (objb)",savefilename)
	savefile = open(savefilename, 'wb') 
	pickle.dump(obj, savefile) 
	print("FILE SAVED")



def loadfromfile(_folder,_name,_type):
	loadfilename = _folder+'/'+_name+'.'+_type+'.objb'
	logs("LOAD FILE (objb)",loadfilename)
	return pickle.load(open(loadfilename, "rb"))
	print("FILE LOADED")

def size(w2v):
	model = 'w2v'
	logs('SIZE of new vocabulary:', str(w2v.corpus_count) )
	print('The vocabulary size of the', model, 'is', len(eval(model).wv.vocab),'\n\n')


def checkinmodel(w2v,newword,erros):
	logs('WORD',newword)
	newwords = formatword(newword)
	predicts = []
	similares = []
	for word in newwords:
		try:
#			if ' ' in word:
#				predicts += w2v.predict_output_word(word.split(' '))
#				predicts += w2v.predict_output_word([word.split(' ')[0]])
#				predicts += w2v.predict_output_word([word.split(' ')[-1]])
#				similares += w2v.most_similar(word.split(' ')[0], topn=5)
#				similares += w2v.most_similar(word.split(' ')[-1], topn=5)
#				print("YES FOUND 2:",word)
#			if ' ' in word:
#				predicts += w2v.predict_output_word(word.split(' '))
#				stopw = create_stopwords()
#				parts =[]
#				for w in word.split(' '):
#					if w in stopw:
#						pass
#					else:
#						parts.append(w)
#				for part in parts:
#					predicts += w2v.predict_output_word([part])
#					similares += w2v.most_similar(part, topn=5)
#					print("YES FOUND PART:",part)
			if ' ' in word:
				validwords = []
				stopw = create_stopwords()
				for w in word.split(' '):
					if w in stopw:
						print("IGNORING: "+w)
					else:
						validwords.append(w)
				predicts += w2v.predict_output_word(validwords)
				similares += w2v.most_similar(validwords)
				print("YES FOUND:",list2string(validwords))
			else:
				predicts += w2v.predict_output_word([word])
				similares += w2v.most_similar(word, topn=5)
				print("YES FOUND:",word)
		except:
			if ' ' in word:
				print("NOT FOUND:",word)
			else:
				erros += 1
				print("NOT FOUND:",word)
				pass
	logs('predicts',content=predicts)
	logs('similares',content=similares)
	return predicts,similares,erros





def checkinmodel_without_prints(w2v,newword,erros,n=1):
	newwords = formatword(newword)
	predicts = []
	similares = []
	for word in newwords:
		try:
			if ' ' in word:
				validwords = []
				stopw = create_stopwords()
				for w in word.split(' '):
					if w in stopw:
						pass
					else:
						validwords.append(w)
				predicts += w2v.predict_output_word(validwords, topn=n)
				similares += w2v.most_similar(validwords, topn=n)
			else:
				predicts += w2v.predict_output_word([word], topn=n)
				similares += w2v.most_similar(word, topn=n)
		except:
			if ' ' in word:
				pass
			else:
				erros += 1
				pass
	return predicts,similares,erros




def formatword(newword):
	if '_' in newword:
		newword = newword.replace('_',' ')
	formats = [newword, newword.capitalize(), newword.upper(), newword.lower()]#, newword.title(), newword.casefold()]
	if normalize('NFKD', newword).encode('ASCII','ignore').decode('ASCII').lower() != newword.lower():
		newword = normalize('NFKD', newword).encode('ASCII','ignore').decode('ASCII')
		formats += [newword, newword.capitalize(), newword.upper(), newword.lower()]#, newword.title(), newword.casefold()]
	return formats



def generate_clean_raw_from_corpus_to_file():
	print("loading corpus ...")
	from nltk.corpus import mac_morpho,floresta
	print("... mac_morpho")
	corpus = mac_morpho.sents()
	print("... floresta")
	corpus += floresta.sents()
	print("clean text")
	rawtext = cleantext(corpus)
	#print("re-sentenizer text")
	#sentences = sentenizer(rawtext)
	text_file = open('texts/'+file,'w')
	text_file.write(rawtext)
	text_file.close()

def save_txt_to_file(file,_type,text):
	logs("Save to txt",file)
	rawtext = cleantext(text)
	text_file = open('texts/'+file+'.'+_type,'w')
	text_file.write(rawtext)
	text_file.close()


def create_stopwords():
	#return []
	stopw = set()
	#words =['a','o','e','i','o','u','um','uma','uns','umas','que','mas']
	#for word in words:
#		stopw.add(word.lower())
	for word in set(stopwords.words('portuguese')):
		stopw.add(word.lower())
		stopw.add(normalize('NFKD', word).encode('ASCII','ignore').decode('ASCII'))
	return stopw



def list2string(list):
	string = ''
	for item in list:
		string +=str(item)+" "
	return string



