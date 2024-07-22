#http://nadbordrozd.github.io/blog/2016/05/20/text-classification-with-word2vec/

#wget http://nlp.stanford.edu/data/glove.6B.zip
#unzip glove.6B.zip

from __future__ import division

import numpy as np
from collections import Counter, defaultdict

import numpy as np
import gensim





from sklearn.pipeline import Pipeline
from sklearn.ensemble import ExtraTreesClassifier

###############################################################################################


class MeanEmbeddingVectorizer(object):
	def __init__(self, word2vec):
		self.word2vec = word2vec
		# if a text is empty we should return a vector of zeros
		# with the same dimensionality as all the other vectors
		self.dim = len(word2vec.itervalues().next())

	def fit(self, X, y):
		return self

	def transform(self, X):
		return np.array([
			np.mean([self.word2vec[w] for w in words if w in self.word2vec]
					or [np.zeros(self.dim)], axis=0)
			for words in X
		])


class TfidfEmbeddingVectorizer(object):
	def __init__(self, word2vec):
		self.word2vec = word2vec
		self.word2weight = None
		self.dim = len(word2vec.itervalues().next())

	def fit(self, X, y):
		tfidf = TfidfVectorizer(analyzer=lambda x: x)
		tfidf.fit(X)
		# if a word was never seen - it must be at least as infrequent
		# as any of the known words - so the default idf is the max of 
		# known idf's
		max_idf = max(tfidf.idf_)
		self.word2weight = defaultdict(
			lambda: max_idf,
			[(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

		return self

	def transform(self, X):
		return np.array([
				np.mean([self.word2vec[w] * self.word2weight[w]
						 for w in words if w in self.word2vec] or
						[np.zeros(self.dim)], axis=0)
				for words in X
			])


class MMGKNB(object):
    def __init__(self, w2v, alpha=1, sigma=1):
        self.alpha = alpha
        self.sigma = sigma
        self.w2v = w2v
        self.vocab = None
        self.priors = {}
        self.class_word_counts = defaultdict(Counter)
        self.class_totals = defaultdict(lambda: 0)

        self.class2vecs = {}
        self.cache = {}

    def vec_loglhood(self, class_, w):
        if w not in self.w2v:
            return 0
        key = (class_, w)
        if key in self.cache:
            return self.cache[key]
        x = self.w2v[w]
        prob = np.exp(-((self.class2vecs[class_] - x)**2/(2 * self.sigma**2)).sum(axis=1)).sum()
        ret = np.log(prob)
        self.cache[key] = ret
        return ret


    def predict_one(self, x):
        scores = {}
        for class_, prior in self.priors.items():
            log_prob = np.log(prior)
            for w in x:
                log_prob += self.vec_loglhood(class_, w)
            scores[class_] = log_prob
        return max(scores.items(), key=lambda z: z[1])[0]

    def predict(self, X):
        return [self.predict_one(x) for x in X]

    def fit(self, X, y):
        self.priors = dict((class_, count/len(y)) for class_, count in Counter(y).items())

        class2vecs = defaultdict(list)
        for x, class_ in zip(X, y):
            self.class_word_counts[class_].update(x)
            self.class_totals[class_] += len(x)

            vectors = [self.w2v[w] for w in x if w in self.w2v]
            class2vecs[class_].extend(vectors)

        self.class2vecs = class2vecs
        for class_ in class2vecs:
            class2vecs[class_] = np.array(class2vecs[class_])

        self.vocab = set(t for x in X for t in x)




class OptimisedMMGKNB(object):
    def __init__(self, w2v, alpha=1, sigma=1):
        self.w2v = w2v
        self.alpha = alpha
        self.sigma = sigma
        self.vocab = None
        self.priors = {}
        self.class_word_counts = defaultdict(Counter)
        self.class_totals = defaultdict(lambda: 0)

        self.class2vecs = {}

    def vec_loglhood(self, class_, x):
        prob = 0
        # for vec in self.class2vecs[class_]:
        #     prob += np.exp(-(x - vec).T.dot(x - vec)/(2 * self.sigma**2))
        prob = np.exp(-((self.class2vecs[class_] - x)**2/(2 * self.sigma**2)).sum(axis=1)).sum()
        return np.log(prob)

    def word_loglhood(self, class_, word):
        lhood = (self.class_word_counts[class_].get(word, 0) + self.alpha) /\
        (self.class_totals[class_] + len(self.vocab) * self.alpha)
        return np.log(lhood)


    def predict_one(self, x):
        scores = {}
        for class_, prior in self.priors.items():
            log_prob = np.log(prior)
            for vec in x['vectors']:
                log_prob += self.vec_loglhood(class_, vec)
            for w in x['words']:
                log_prob += self.word_loglhood(class_, w)
            scores[class_] = log_prob
        return max(scores.items(), key=lambda x: x[1])[0]

    def predict(self, X):
        return [self.predict_one(x) for x in X]

    def fit(self, X, y):
        self.priors = dict((class_, count/len(y)) for class_, count in Counter(y).items())

        class2vecs = defaultdict(list)
        for x, class_ in zip(X, y):
            self.class_word_counts[class_].update(x['words'])
            self.class_totals[class_] += len(x)

            vectors = x['vectors']
            class2vecs[class_].extend(vectors)

        self.class2vecs = class2vecs
        for class_ in class2vecs:
            class2vecs[class_] = np.array(class2vecs[class_])

        self.vocab = set(t for x in X for t in x['words'])

##############################################################################################




DEBUG = True


if DEBUG:
	#LOAD A PRE-TRAINED MODEL
	with open("texts/glove/glove.6B.50d.txt", "rb") as lines:
		w2v = {line.split()[0]: np.array(map(float, line.split()[1:]))
			   for line in lines}
else:
	#CREATE A NEW MODEL
	# let X be a list of tokenized texts (i.e. list of lists of tokens)
	model = gensim.models.Word2Vec(X, size=100)
	w2v = dict(zip(model.wv.index2word, model.wv.syn0))






'''
etree_w2v = Pipeline([
	("word2vec vectorizer", MeanEmbeddingVectorizer(w2v)),
	("extra trees", ExtraTreesClassifier(n_estimators=200))])
etree_w2v_tfidf = Pipeline([
	("word2vec vectorizer", TfidfEmbeddingVectorizer(w2v)),
	("extra trees", ExtraTreesClassifier(n_estimators=200))])
'''


X = [['Berlin', 'London'],['cow', 'cat'],['pink', 'yellow']]
y = ['capitals', 'animals', 'colors']


etree_glove_big = OptimisedMMGKNB(w2v)
etree_glove_big.fit(X, y)

# never before seen words!!!
test_X = [['dog'], ['red'], ['Madrid']]

print (etree_glove_big.predict(test_X))
