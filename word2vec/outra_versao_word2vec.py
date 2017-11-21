#http://nbviewer.jupyter.org/github/danielfrg/word2vec/blob/master/examples/word2vec.ipynb
#pip install word2vec

import word2vec


########## Training
file='text8'

#word2vec.word2phrase('texts/'+file, 'texts/'+file+'-phrases', verbose=True)
#word2vec.word2vec('texts/'+file+'-phrases', 'texts/'+file+'.bin', size=100, verbose=True)
word2vec.word2clusters('texts/'+file, 'texts/'+file+'-clusters.txt', 100, verbose=True)



########## Predictions
model = word2vec.load('texts/'+file+'.bin', encoding = "ISO-8859-1")
#model.vocab
#model.vectors.shape
#model.vectors
#model['dog'].shape
#model['dog'][:10]
word1='dog'
indexes, metrics = model.cosine(word1)
#model.vocab[indexes]
#model.generate_response(indexes, metrics)
print ( "model.cosine('"+word1+"')" )
print ( model.generate_response( indexes, metrics ).tolist() )




########## Phrases
word2='los_angeles'
indexes, metrics = model.cosine(word2)
print ( "model.cosine('"+word2+"')" )
print ( model.generate_response(indexes, metrics).tolist() )



########## Analogies
indexes, metrics = model.analogy(pos=['king', 'woman'], neg=['man'], n=10)
print ( "model.analogy(pos=['king', 'woman'], neg=['man'], n=10)" )
print ( model.generate_response(indexes, metrics).tolist() )




########## Clusters
clusters = word2vec.load_clusters('texts/'+file+'-clusters.txt')
clusters[word1]
clusters.get_words_on_cluster(90).shape
clusters.get_words_on_cluster(90)[:10]
model.clusters = clusters
indexes, metrics = model.analogy(pos=['paris', 'germany'], neg=['france'], n=10)
print ( "model.analogy(pos=['paris', 'germany'], neg=['france'], n=10)" )
print ( model.generate_response(indexes, metrics).tolist() )





'''
limit=1
i=0
insert = []
with open("texts/"+file, "r") as ins:
	for line in ins:
		if i>limit:
			break
		line = line.strip()
		#print(line)
		insert.append([(line,"CIDADE")])
		i=i+1
print(insert)
'''