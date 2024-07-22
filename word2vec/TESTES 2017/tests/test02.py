#https://rare-technologies.com/word2vec-tutorial/
#http://iamaziz.github.io/blog/2015/11/02/word2vec-with-nltk-retrain-and-evaluate/
#https://radimrehurek.com/gensim/models/word2vec.html

#IMPORT
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim.models import Word2Vec
from nltk.corpus import mac_morpho,floresta
import pickle

#CREATE W2V
#mac = Word2Vec(mac_morpho.sents())
#flor = Word2Vec(floresta.sents())

#SAVE FILES
#filename1 = 'W2V/mac.W2V.objb'
#filename2 = 'W2V/flor.W2V.objb'
#file1 = open(filename1, 'wb') 
#file2 = open(filename2, 'wb') 
#pickle.dump(mac, file1) 
#pickle.dump(flor, file2) 


#LOAD FILES
mac = pickle.load(open('W2V/mac.W2V.objb', "rb"))
flor = pickle.load(open('W2V/flor.W2V.objb', "rb"))


#USES
print ( mac.most_similar('São', topn=5) )
print ( mac.most_similar('presidente', topn=5) )
print ( mac.most_similar('cidade', topn=5) )
print ( flor.most_similar('Porto', topn=5) )
print ( flor.most_similar('Estado', topn=5) )
print ( mac.predict_output_word(['presidente']) )
print ( mac.predict_output_word(['Rio','de']) )

