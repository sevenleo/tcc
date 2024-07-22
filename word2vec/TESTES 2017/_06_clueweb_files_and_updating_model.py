#https://radimrehurek.com/gensim/models/word2vec.html
#https://codesachin.wordpress.com/2015/10/09/generating-a-word2vec-model-from-a-block-of-text-using-gensim-python/
#https://radimrehurek.com/gensim/models/doc2vec.html

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
		text = re.sub("[^a-zA-Z1-9]+", "", text)
		text = re.sub(r"[']", '', text)
		text = re.sub(r"ˈ", '', text)
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

def search(word):
	_type = 'string'
	folder = 'SEARCH'
	name = word
	try:
		text = loadfromfile(folder,name,_type)
		return text
	except:
		import wikipedia
		#wikipedia.set_lang("pt")
		results = wikipedia.search(newword)
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

def size():
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
			predicts += w2v.predict_output_word([word])
			similares += w2v.most_similar(word, topn=5)
			print("YES FOUND:",word)
		except:
			erros += 1
			print("NOT FOUND:",word)
			pass
	logs('predicts',content=predicts)
	logs('similares',content=similares)
	return predicts,similares,erros




def formatword(newword):
	return [newword, newword.capitalize(), newword.upper(), newword.lower(), newword.title(), newword.casefold()]



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

def create_stopwords():
	#return []
	stopw = set()
	#words =['a','o','e','i','o','u','um','uma','uns','umas','que','mas']
	#for word in words:
#		stopw.add(word.lower())
	for word in set(nltk.corpus.stopwords.words('portuguese')):
		stopw.add(word.lower())
		stopw.add(normalize('NFKD', word).encode('ASCII','ignore').decode('ASCII'))
	return stopw







#IMPORT
logs("IMPORT")
import nltk
import glob
import re
import os
import pickle
import logging
from multiprocessing import cpu_count
from unicodedata import normalize



lang='pt'
file = 'clueweb-part-m-00001'
level=1
erros = 0

stopw = create_stopwords()


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence


try:
	#LOAD FILES
	try:
		loadfilename = 'W2V'+'/'+file+'.model'
		logs("LOAD FILE (model)",loadfilename)
		w2v = Word2Vec.load(loadfilename)
		print("FILE LOADED")
	except:
		print(file+".model FILE NOT EXIST")
		w2v = loadfromfile('W2V',file,'W2V')
except:
	erros += 1
	print("**** ERRO = {}".format(erros))
	print(file+".objb FILE NOT EXIST")
	print("FILE CANNOT BE LOADED")
	#CREATE W2V
	logs("CREATE W2V",file)
	


	#load text preprocessed
	##sentences = LineSentence('myfile.txt')
	sentences = LineSentence('texts/'+file)
	##sentences = LineSentence('texts/'+file+'.bz2')
	##sentences = LineSentence('texts/'+file+'.gz')


	#create model
	if level==0:
		w2v = Word2Vec(sentences)

	elif level==1:
		min_word_count = 0
		num_workers = cpu_count()
		w2v = Word2Vec(
		    workers=num_workers,
		    min_count=min_word_count
		)
		w2v.build_vocab(sentences)
		w2v.train(sentences,total_examples=w2v.corpus_count, epochs=w2v.iter)

	else:

		#https://github.com/llSourcell/word_vectors_game_of_thrones-LIVE/blob/master/Thrones2Vec.ipynb
		#ONCE we have vectors
		#step 3 - build model
		#3 main tasks that vectors help with
		#DISTANCE, SIMILARITY, RANKING

		# Dimensionality of the resulting word vectors.
		#more dimensions, more computationally expensive to train
		#but also more accurate
		#more dimensions = more generalized
		num_features = 300
		# Minimum word count threshold.
		min_word_count = 3

		# Number of threads to run in parallel.
		#more workers, faster we train
		num_workers = cpu_count()

		# Context window length.
		context_size = 7

		# Downsample setting for frequent words.
		#0 - 1e-5 is good for this
		downsampling = 1e-3

		# Seed for the RNG, to make the results reproducible.
		#random number generator
		#deterministic, good for debugging
		seed = 1

		w2v = Word2Vec(
		    sg=1,
		    seed=seed,
		    workers=num_workers,
		    size=num_features,
		    min_count=min_word_count,
		    window=context_size,
		    sample=downsampling
		)


		w2v.build_vocab(sentences)
		w2v.train(sentences,total_examples=w2v.corpus_count, epochs=w2v.iter)





	#SAVE FILES
	try:
		savefilename = 'W2V'+'/'+file+'.model'
		logs("SAVE FILE (model)",savefilename)
		w2v.save(savefilename)
		print("FILE SAVED")
	except:
		erros += 1
		print("**** ERRO = {}".format(erros))
		print(file+".model FILE CANNOT BE SAVED")
		saveinfile(w2v,W2V,file,W2V)

size()





#USES
#newwords = ['CIDADE','ESTADO','PRESIDENTE','casal','goiania','recife']
newwords = ['azul']


print("model.corpus_count")
print(w2v.corpus_count)
print("model.iter")
print(w2v.iter)

for newword in newwords:
	predicts,similares,erros = checkinmodel(w2v,newword,erros)



newsentences = LineSentence('texts/random.txt')
w2v.build_vocab(newsentences, update=True)
w2v.train(newsentences, total_examples=w2v.corpus_count, epochs=w2v.iter)

print("model.corpus_count")
print(w2v.corpus_count)
print("model.iter")
print(w2v.iter)


for newword in newwords:
	predicts,similares,erros = checkinmodel(w2v,newword,erros)


