#https://rare-technologies.com/word2vec-tutorial/




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
