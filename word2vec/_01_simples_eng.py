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
	lang = "english"
	for word in nltk.word_tokenize(frase, lang):
			#tokens.append(word.decode("utf-8"))
			tokens.append(word)
	return tokens

def sentenizer(text):
	lang = "english"
	sentences = nltk.sent_tokenize(text,language=lang)
	print("Number of senteces:  "+str(len(sentences)))
	return sentences

def cleantext(text):
	text = text.replace("\n",". ") ##TROCAR POR EXPRESSAO REGULAR, POIS É MAIS RAPIDO
	#EX.:text = re.sub(r'[\\n]', '.', text)
	text = re.sub(r"[']", '', text)
	text = re.sub(r"ˈ", '', text)
	return text

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
	newwords = [newword, newword.capitalize(), newword.upper(), newword.lower(), newword.title(), newword.casefold()]
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















#IMPORT
logs("IMPORT")
import nltk
import glob
import re
import os
import pickle
import logging
from multiprocessing import cpu_count



lang='eng'
file = 'text8.eng'
level=1
erros = 0


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim.models import Word2Vec


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
	
	from gensim.models.word2vec import LineSentence
	##sentences = LineSentence('myfile.txt')
	##sentences = LineSentence('compressed_text.txt.bz2')
	##sentences = LineSentence('compressed_text.txt.gz')


	#only one file
	sentences = LineSentence('texts/'+file)

	##all files in language
	#	sentences = ""
	#	files = sorted(glob.glob("texts/*."+lang))
	#	for file in files:
	#		sentences = sentences+LineSentence('texts/'+file)
	
	##especific namefile
	#	sentences = ""
	#	files = sorted(glob.glob("texts/*"+file+"*"))
	#	for file in files: 
	#		sentences = sentences + LineSentence('texts/'+file)
	
	##especific type
	#	sentences = ""
	#	files = sorted(glob.glob("texts/*.txt*"))
	#	for file in files: 
	#		sentences = sentences + LineSentence('texts/'+file)


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
try:
	logs("SIMILAR")
	print("DOG")
	print ( w2v.most_similar('dog', topn=5) )
	print("LOS ANGELES")
	print ( w2v.most_similar('chicago', topn=5) )
	logs("PREDICT")
	print("LOS ANGELES")
	print ( w2v.predict_output_word(['los','angeles']) )
except:
	pass