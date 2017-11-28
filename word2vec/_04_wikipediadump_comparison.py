#https://markroxor.github.io/gensim/static/notebooks/online_w2v_tutorial.html


from gensim.corpora.wikicorpus import WikiCorpus
from gensim.models.word2vec import Word2Vec, LineSentence
from pprint import pprint
from copy import deepcopy
from multiprocessing import cpu_count




old, new = [  WikiCorpus('enwiki-{}-pages-articles.xml.bz2'.format(ymd)) for ymd in ['20101011', '20160820']  ]

def write_wiki(wiki, name, titles = []):
    with open('{}.wiki'.format(name), 'wb') as f:
        wiki.metadata = True
        for text, (page_id, title) in wiki.get_texts():
            if title not in titles:
                f.write(b' '.join(text)+b'\n')
                titles.append(title)
    return titles


old_titles = write_wiki(old, 'old')
all_titles = write_wiki(new, 'new', old_titles)


oldwiki, newwiki = [LineSentence(f+'.wiki') for f in ['old', 'new']]





%%time
model = Word2Vec(oldwiki, min_count = 0, workers=cpu_count())
# model = Word2Vec.load('oldmodel')
oldmodel = deepcopy(model)
oldmodel.save('oldmodel')


try:
    print(oldmodel.most_similar('babymetal'))
except KeyError as e:
    print(e)


%%time
model.build_vocab(newwiki, update=True)
model.train(newwiki)
model.save('newmodel')
# model = Word2Vec.load('newmodel')


for m in ['oldmodel', 'model']:
    print('The vocabulary size of the', m, 'is', len(eval(m).vocab))


try:
    pprint(model.most_similar('babymetal'))
except KeyError as e:
    print(e)


w = 'zootopia'
for m in ['oldmodel', 'model']:
    print('The count of the word,'+w+', is', eval(m).vocab[w].count, 'in', m)
    pprint(eval(m).most_similar(w))
    print('')

