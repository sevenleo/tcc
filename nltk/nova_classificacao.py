from nltk.corpus import mac_morpho
from collections import defaultdict
import pickle



translate = {
    #'N|AP' :'NUM',
    #'N|DAD' :'NUM',
    #'N|DAT' :'NUM',
    #'N|HOR' :'NUM',
    #'N|TEL' :'NUM',
    '!' :   'EXCLAMACAO',
    ',' :   'VIRGULA',
    '.' :   'PONTO',  
    '?' :   'INTERROGACAO', 
    'adj': "ADJ",
    'ADJ': 'ADJ',
    'adv': "ADV",
    'ADV': 'ADV',
    'adv-ks': "ADV",
    'ADV-KS': 'ADV',
    'adv-ks-rel': "ADV",
    'ADV-KS-REL': 'ADV',
    'ap': "NUM",
    'AP': 'AP',
    'art': "ART",
    'ART': 'ART',
    'conj-c': "CONJ",
    'conj-p': "CONJ",
    'conj-s': "CONJ",
    'cur': "MOEDA",
    'CUR': 'MOEDA',
    'dad': "NUM",
    'DAD': 'DAD',
    'dat': "NUM",
    'DAT': 'DAT',
    'ec': "PRT",  ############
    'est': "SUBST",
    'EST': 'EST',  ############
    'hor': "NUM",
    'HOR': 'HOR',
    'in': "X",  ############
    'IN': 'INT',
    'kc': "ADP",
    'KC': 'CONJ',
    'ks': "ADP",
    'KS': 'CONJ',
    'n': "SUBST",
    'N': 'SUBST',
    'npro': "NOUN",
    'nprop': "NPROP",
    'NPROP': 'NPROP',
    'num': "NUM",
    'NUM': 'NUM',
    'pcp': "V",
    'PCP': 'V',
    'pden': "ADV",
    'PDEN': 'DENOTATIVA',  ############
    'pp': "PREP",
    'prep': "PREP",
    'PREP': 'PREP',
    'pro-ks': "PRON",
    'PRO-KS': 'PRON',
    'pro-ks-rel': "PRON",
    'PRO-KS-REL': 'PRON',
    'proadj': "PRON",
    'PROADJ': 'PRON',
    'pron-det': "PRON",
    'pron-indp': "PRON",
    'pron-pers': "PRON",
    'prop': "NPROP",
    'propess': "PRON",
    'PROPESS': 'PRON',
    'prosub': "PRON",
    'PROSUB': 'PRON',
    'prp': "PREP",
    'prp-': "NPROP",
    'tel': "NUM",
    'TEL': 'TEL',
    'v': "V",
    'V': 'V',
    'v-fin': "V",
    'v-ger': "V",
    'v-inf': "V",
    'v-pcp': "V",
    'vaux': "V",
    'VAUX': 'V',
    'vp': "V",
}

translate = defaultdict(lambda: "__", translate)

##############################################################


i=0;

import random
sents = 10#random.randint(0,100)




print ("=============LOADING==============================\n...")
try:
    file = open('dicio_tag.obj', 'rb') 
    wiki = pickle.load(file) 
except EOFError:#open('dicio_tag.obj', 'r')
    wiki = []
except IOError:#open('dicio_tag.obj', 'rb')
    wiki = []


print ("=============PROCESSANDO=============================")
for sent in mac_morpho.tagged_sents():
    newsent=[]
    for word in sent:
        baseclass = word[1].split('|')[0]
        newclass = translate[baseclass]
        palavra = word[0]
        newsent.append((palavra,newclass))
    wiki.append(newsent)
    i=i+1
    if i>=sents:
        break

print ("=============FINAL==============================")
print (wiki)
print ("\nTotal de frases: "+str(len(wiki)))


print ("=============SAVING==============================\n...")

file = open('dicio_tag.obj', 'wb') 
pickle.dump(wiki, file) 







#print ("=============TEST==============================")
#print ("\nORIGINAL:")
#print (mac_morpho.tagged_sents()[sents-1])
#print ("\nWIKI:")




"""
Estou prestes a escrever um arquivo muito grande, pretendo manipula-lo com pickle:
#SAVE
file = open('dicio_tag.obj', 'wb') 
pickle.dump(wiki, file) 

#LOAD
file = open('dicio_tag.obj', 'rb') 
wiki = pickle.load(file) 

Existem bibliotecas melhores que a pickle?
Qual o melhor método para salva-lo e para lê-lo da forma mais rápida, sem consumir muitos recursos e com que ele fique do menor tamanho possivel.
"""