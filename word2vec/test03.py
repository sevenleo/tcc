
#https://radimrehurek.com/gensim/models/word2vec.html
#https://codesachin.wordpress.com/2015/10/09/generating-a-word2vec-model-from-a-block-of-text-using-gensim-python/
#https://radimrehurek.com/gensim/models/doc2vec.html

def logs(titulo,texto="",texto2=""):
	log = "\n\n"
	log = "\n\n---------------------------------------\n"
	log = log + titulo
	log = log + " :\t"+texto
	if texto2 != "":
		log = log + "\n"+texto2+""
	log = log + "\n---------------------------------------\n"
	print (log)

def tokenize(frase):
	tokens=[]
	lang = "portuguese"
	lang = "english"
	for word in nltk.word_tokenize(frase, lang):
			#tokens.append(word.decode("utf-8"))
			tokens.append(word)
	return tokens

def sentenizer(text):
	lang = "portuguese"
	lang = "english"
	sentences = nltk.sent_tokenize(text,language=lang)
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
	savefilename = _folder+'/'+_name+'.'+_type+'.objb'
	logs("SAVE FILE (objb)",savefilename)
	savefile = open(savefilename, 'wb') 
	pickle.dump(obj, savefile) 


def loadfromfile(_folder,_name,_type):
	loadfilename = _folder+'/'+_name+'.'+_type+'.objb'
	logs("LOAD FILE (objb)",loadfilename)
	return pickle.load(open(loadfilename, "rb"))

#IMPORT
logs("IMPORT")
import nltk
import re
import pickle
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
onlinesearch=True
file = 'text8'



from gensim.models import Word2Vec


try:
	#LOAD FILES
	try:
		loadfilename = 'W2V'+'/'+file+'.model'
		logs("LOAD FILE (model)",loadfilename)
		w2v.load(loadfilename)
	except:
		print("model FILE NOT EXIST")
		w2v = loadfromfile('W2V',file,'W2V')
except:
	print("FILE CANNOT BE LOADED")
	#CREATE W2V
	logs("CREATE W2V",file)
	
	from gensim.models.word2vec import LineSentence
	##sentences = LineSentence('myfile.txt')
	##sentences = LineSentence('compressed_text.txt.bz2')
	##sentences = LineSentence('compressed_text.txt.gz')

	sentences = LineSentence('texts/'+file)
	w2v = Word2Vec(sentences)


	#SAVE FILES
	try:
		savefilename = 'W2V'+'/'+file+'.model'
		logs("SAVE FILE (model)",savefilename)
		w2v.save(savefilename)
	except:
		print("model FILE CANNOT BE SAVED")
		saveinfile(w2v,W2V,file,W2V)


#USES
logs("SIMILAR")
print("DOG")
print ( w2v.most_similar('dog', topn=5) )
print("LOS ANGELES")
print ( w2v.most_similar('chicago', topn=5) )

logs("PREDICT")
print("LOS ANGELES")
print ( w2v.predict_output_word(['los','angeles']) )


#NEW SENTENCES
logs("NEW SENTENCES","with Wikipedia","http://wikipedia.readthedocs.io/en/latest/quickstart.html")
newword = 'xuxa'

if onlinesearch:
	text = search(newword)
	text = cleantext(text)
	new_sentences = sentenizer(text)

else:
	new_sentences = LineSentence('texts/'+newword)


#SHOW
#logs("SHOW RESULTS")
#for s in new_sentences:
#	print('\n')
#	print(s)
#	print('\n')


#TEST NEW SENTENCES
logs("TEST NEW SENTENCES",newword)
try:
	w2v.build_vocab(new_sentences, update=True)
	w2v.train(new_sentences,total_examples=w2v.corpus_count, epochs=w2v.iter)
	print ( w2v.most_similar(newword, topn=5) )
	print ( w2v.predict_output_word([newword]) )
except:
	pass


