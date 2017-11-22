
#https://radimrehurek.com/gensim/models/word2vec.html

#IMPORT
print("_________ IMPORT _________")
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim.models import Word2Vec
import pickle

#CREATE W2V
print("_________ CREATE W2V _________")
#sentences = LineSentence('myfile.txt')
#sentences = LineSentence('compressed_text.txt.bz2')
#sentences = LineSentence('compressed_text.txt.gz')
file='text8'
sentences = Word2Vec.LineSentence('texts/'+file)
text8 = Word2Vec(sentences)

#SAVE FILES
print("_________  FILES SAVE _________")
filename1 = 'W2V/text8.W2V.objb'
file1 = open(filename1, 'wb') 
pickle.dump(mac, file1) 


#LOAD FILES
print("_________  FILES LOAD _________")
#mac = pickle.load(open('W2V/mac.W2V.objb', "rb"))
#flor = pickle.load(open('W2V/flor.W2V.objb', "rb"))


#USES
print("_________ USES _________")
print("DOG")
print ( text8.most_similar('dog', topn=5) )
print("LOS ANGELES")
print ( text8.most_similar('los_angeles', topn=5) )
print("LOS ANGELES")
print ( text8.predict_output_word(['los','angeles']) )
