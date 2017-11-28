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


def showtime():
    if DEBUG:
        debugcount+=1
        print('Passo:',debug)
        print("\nTempo de execucao: "+str(time.time() - start)+" seg")




#test with a small part
#or
#full content

#latest = WikiCorpus('texts/wikipedia/ptwiki-{}-pages-articles1.xml.bz2'.format('latest'))
latest = WikiCorpus('texts/wikipedia/ptwiki-{}-pages-articles.xml.bz2'.format('latest'))
showtime()


#wikipt_titles = write_wiki(latest, 'latest1')
wikipt_titles = write_wiki(latest, 'latest')
showtime()


#latestwiki = LineSentence('texts/wikipedia/latest1.wiki')
latestwiki = LineSentence('texts/wikipedia/latest.wiki')
showtime()


model = Word2Vec(latestwiki, min_count = 0, workers=cpu_count())
showtime()


# model = Word2Vec.load('oldmodel')
latestwiki = deepcopy(model)
showtime()


latestwiki.save('W2V/wikipedia.model')
showtime()


try:
    print(latestwiki.most_similar('Ronaldo'))
except KeyError as e:
    print(e)
showtime()