
#https://radimrehurek.com/gensim/models/word2vec.html
#https://codesachin.wordpress.com/2015/10/09/generating-a-word2vec-model-from-a-block-of-text-using-gensim-python/
#https://radimrehurek.com/gensim/models/doc2vec.html

#IMPORT
print("_________ IMPORT _________")
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim.models import Word2Vec

import pickle
file = 'text8'
load = True


if load == False:
	#CREATE W2V
	print("_________ CREATE W2V :"+file+"_________")
	
	from gensim.models.word2vec import LineSentence
	##sentences = LineSentence('myfile.txt')
	##sentences = LineSentence('compressed_text.txt.bz2')
	##sentences = LineSentence('compressed_text.txt.gz')

	sentences = LineSentence('texts/'+file)
	w2v = Word2Vec(sentences)


	#SAVE FILES
	savefilename = 'W2V/'+file+'.W2V.objb'
	print("_________  SAVE FILE :"+savefilename+" _________")
	savefile = open(savefilename, 'wb') 
	pickle.dump(w2v, savefile) 

else:
	#LOAD FILES
	print("_________  LOAD FILE :"+file+"_________")
	w2v = pickle.load(open('W2V/'+file+'.W2V.objb', "rb"))

#USES
print("_________ EXEMPLOS _________")
print("DOG")
print ( w2v.most_similar('dog', topn=5) )
print("LOS ANGELES")
print ( w2v.predict_output_word(['los','angeles']) )
print("LOS ANGELES")
print ( w2v.most_similar('chicago', topn=5) )
