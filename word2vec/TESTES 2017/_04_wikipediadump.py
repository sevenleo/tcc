#https://markroxor.github.io/gensim/static/notebooks/online_w2v_tutorial.html
#Download wikipedia:
#https://dumps.wikimedia.org/

#Portugues:
#https://dumps.wikimedia.org/other/static_html_dumps/current/pt/wikipedia-pt-html.tar.7z

#https://dumps.wikimedia.org/ptwiki/latest/
#https://dumps.wikimedia.org/ptwiki/latest/ptwiki-latest-pages-articles.xml.bz2


from gensim.corpora.wikicorpus import WikiCorpus
from gensim.models.word2vec import Word2Vec, LineSentence
from pprint import pprint
from copy import deepcopy
from multiprocessing import cpu_count
import time
start = time.time()
DEBUG=True
debugcount = 0


def write_wiki(wiki, name, titles = []):
    with open('texts/wikipedia/{}.wiki'.format(name), 'w') as f:
        wiki.metadata = True
        for text, (page_id, title) in wiki.get_texts():
            if title not in titles:
                #f.write(b' '.join(text)+b'\n')
                f.write(' '.join(text)+'\n')
                #f.write(text)
                #f.write('\n')
                titles.append(title)
    return titles


def showtime(debugcount):
    if DEBUG:
        debugcount+=1
        print('Passo:',debugcount)
        print("\nTempo de execucao: "+str(time.time() - start)+" seg")
    return debugcount



debugcount = showtime(debugcount)


#test with a small part
#or
#full content

#latest = WikiCorpus('texts/wikipedia/ptwiki-{}-pages-articles1.xml.bz2'.format('latest'))
latest = WikiCorpus('texts/wikipedia/ptwiki-{}-pages-articles.xml.bz2'.format('latest'))
debugcount = showtime(debugcount)


#wikipt_titles = write_wiki(latest, 'latest1')
wikipt_titles = write_wiki(latest, 'latest')
debugcount = showtime(debugcount)


#latestwiki = LineSentence('texts/wikipedia/latest1.wiki')
latestwiki = LineSentence('texts/wikipedia/latest.wiki')
debugcount = showtime(debugcount)


model = Word2Vec(latestwiki, min_count = 0, workers=cpu_count())
debugcount = showtime(debugcount)


# model = Word2Vec.load('oldmodel')
latestwiki = deepcopy(model)
debugcount = showtime(debugcount)


latestwiki.save('W2V/wikipedia.model')
debugcount = showtime(debugcount)


try:
    print(latestwiki.most_similar('Ronaldo'))
except KeyError as e:
    print(e)
debugcount = showtime(debugcount)




#Core i5-2500 10GB de Ram
#python _04_wikipediadump.py
#Passo: 1
#
#Tempo de execucao: 0.0003809928894042969 seg
#Passo: 2
#
#Tempo de execucao: 1179.525761127472 seg
#^[[B
#Passo: 3
#
#Tempo de execucao: 12752.977465629578 seg
#Passo: 4
#
#Tempo de execucao: 12752.986975431442 seg
#Passo: 5
#
#Tempo de execucao: 14142.166020870209 seg
#Passo: 6
#
#Tempo de execucao: 14196.124321699142 seg
#Passo: 7
#
#Tempo de execucao: 14214.564305067062 seg
#"word 'Ronaldo' not in vocabulary"
#Passo: 8
#
#Tempo de execucao: 14218.143342256546 seg