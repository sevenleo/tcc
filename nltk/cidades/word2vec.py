#https://rare-technologies.com/word2vec-tutorial/



'''
# import modules & set up logging
import gensim, logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
 
sentences = [['first', 'sentence'], ['second', 'sentence']]
# train word2vec on the two sentences
#default > model = gensim.models.Word2Vec(sentences, min_count=5, iter=5,size=100,workers=1)
model = gensim.models.Word2Vec(sentences, min_count=1, iter=5,size=100,workers=8)

# min_count = Words that appear only once or twice in a billion-word corpus are probably uninteresting typos and garbage. In addition, there’s not enough data to make any meaningful training on those words, so it’s best to ignore them
# iter = calling Word2Vec(sentences, iter=1) will run two passes over the sentences iterator (or, in general iter+1 passes; default iter=5). The first pass collects words and their frequencies to build an internal dictionary tree structure
# size = Another parameter is the size of the NN layers, which correspond to the “degrees” of freedom the training algorithm has. Bigger size values require more training data, but can lead to better (more accurate) models. Reasonable values are in the tens to hundreds.
# workers = cores usados,default=1, instalar cython para usar mais de um
# https://radimrehurek.com/gensim/models/word2vec.html#gensim.models.word2vec.Word2Vec


model.save('/tmp/mymodel')
new_model = gensim.models.Word2Vec.load('/tmp/mymodel')
# you can load models created by the original C tool, both using its text and binary formats
#model = Word2Vec.load_word2vec_format('/tmp/vectors.txt', binary=False)
# using gzipped/bz2 input works too, no need to unzip:
#model = Word2Vec.load_word2vec_format('/tmp/vectors.bin.gz', binary=True)


#model.train(more_sentences)
#You may need to tweak the total_words parameter to train(), depending on what learning rate decay you want to simulate.

model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
#[('queen', 0.50882536)]
model.doesnt_match("breakfast cereal dinner lunch".split())
#'cereal'
model.similarity('woman', 'man')
#0.73723527

model['first']  # raw NumPy vector of a word
#array([-0.00449447, -0.00310097,  0.02421786, ...], dtype=float32)
'''




'''
from gensim.models import Word2Vec
from nltk.corpus import mac_morpho


mac = mac_morpho.sents()
flor = nltk.corpus.floresta.tagged_sents()

vectorize_mac = Word2Vec(mac,workers=8)
vectorize_flor = Word2Vec(flor,workers=8)

print(vectorize_mac.most_similar('comida', topn=5))
print(vectorize_flor.most_similar('comida', topn=5))
'''


'''
from gensim.models import Word2Vec
#from nltk.corpus import mac_morpho

sents = [['Jersei', 'atinge', 'média', 'de', '5'],['Jersei', 'atinge']]
model = Word2Vec(sents, size=100, window=5, min_count=1, workers=4)

print(model.most_similar('de', topn=10))

print(model.predict_output_word(['Jersei']))
'''






'''

from gensim.models import Word2Vec
from nltk.corpus import mac_morpho,floresta
b = Word2Vec(brown.sents()[:100])
t = Word2Vec(floresta.sents()[:100])

b.most_similar('money', topn=5)
t.most_similar('money', topn=5)
b.most_similar('great', topn=5)
t.most_similar('great', topn=5)
b.most_similar('company', topn=5)
t.most_similar('company', topn=5)
'''

import word2vec


########## Training
word2vec.word2phrase('/Users/drodriguez/Downloads/text8', '/Users/drodriguez/Downloads/text8-phrases', verbose=True)
word2vec.word2vec('/Users/drodriguez/Downloads/text8-phrases', '/Users/drodriguez/Downloads/text8.bin', size=100, verbose=True)
word2vec.word2clusters('/Users/drodriguez/Downloads/text8', '/Users/drodriguez/Downloads/text8-clusters.txt', 100, verbose=True)




########## Predictions
model = word2vec.load('/Users/drodriguez/Downloads/text8.bin')
#model.vocab
#model.vectors.shape
#model.vectors
#model['dog'].shape
#model['dog'][:10]
indexes, metrics = model.cosine('socks')
model.vocab[indexes]
#model.generate_response(indexes, metrics)
print ( "model.cosine('socks')" )
print ( model.generate_response(indexes, metrics).tolist() )




########## Phrases
indexes, metrics = model.cosine('los_angeles')
print ( "model.cosine('los_angeles')" )
print ( model.generate_response(indexes, metrics).tolist() )




########## Analogies
indexes, metrics = model.analogy(pos=['king', 'woman'], neg=['man'], n=10)
print ( "model.analogy(pos=['king', 'woman'], neg=['man'], n=10)" )
print ( model.generate_response(indexes, metrics).tolist() )




########## Clusters
clusters = word2vec.load_clusters('/Users/drodriguez/Downloads/text8-clusters.txt')
clusters['dog']
clusters.get_words_on_cluster(90).shape
clusters.get_words_on_cluster(90)[:10]
model.clusters = clusters
indexes, metrics = model.analogy(pos=['paris', 'germany'], neg=['france'], n=10)
print ( "model.analogy(pos=['paris', 'germany'], neg=['france'], n=10)" )
print ( model.generate_response(indexes, metrics).tolist() )