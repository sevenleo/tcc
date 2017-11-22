
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
    for word in nltk.word_tokenize(frase, lang):
            #tokens.append(word.decode("utf-8"))
            tokens.append(word)
    return tokens

def sentenizer(text):
	sentences = nltk.sent_tokenize(text)
	return sentences

def cleantext(text):
	text = re.sub(r'[\.]', '', text)
	text = re.sub(r"[']", '', text)
	text = re.sub(r"ˈ", '', text)
	return text

#IMPORT
logs("IMPORT")
import nltk
import re
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim.models import Word2Vec

import pickle
file = 'text8'
load = True
onlinesearch=True

if load == False:
	#CREATE W2V
	logs("CREATE W2V",file)
	
	from gensim.models.word2vec import LineSentence
	##sentences = LineSentence('myfile.txt')
	##sentences = LineSentence('compressed_text.txt.bz2')
	##sentences = LineSentence('compressed_text.txt.gz')

	sentences = LineSentence('texts/'+file)
	w2v = Word2Vec(sentences)


	#SAVE FILES
	savefilename = 'W2V/'+file+'.W2V.objb'
	logs("SAVE FILE",savefilename)
	savefile = open(savefilename, 'wb') 
	pickle.dump(w2v, savefile) 

else:
	#LOAD FILES
	loadfilename = 'W2V/'+file+'.W2V.objb'
	logs("LOAD FILE",loadfilename)
	w2v = pickle.load(open(loadfilename, "rb"))

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
	import wikipedia
	#wikipedia.set_lang("pt")
	results = wikipedia.search(newword)
	page = wikipedia.page(results[0])
	#text = wikipedia.summary(newword)
	text = page.content
	text = cleantext(text)
	new_sentences = sentenizer(text)

else:
	new_sentences = LineSentence('texts/'+newword)
print(text)
print(len(new_sentences))
print(len(new_sentences))
print(len(new_sentences))
print(new_sentences)
w2v.build_vocab(new_sentences, update=True)
w2v.train(new_sentences)
print ( w2v.most_similar(newword, topn=5) )
print ( w2v.predict_output_word([newword]) )
