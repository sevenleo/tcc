print ("==========================INICIALIZANDO AMBIENTE\n...")
from nltk.corpus import mac_morpho
from nltk.corpus import floresta
from collections import defaultdict
#import pickle
import json

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
    'ADJ': 'ADJETIVO',
    'ADV': 'ADVERBIO',
    'ADV-KS': 'ADVERBIO',
    'ADV-KS-REL': 'ADVERBIO',
    'AP': 'APOSTO',
    'ART': 'ARTIGO',
    'CONJ-C': 'CONJUNCAO',
    'CONJ-P': 'CONJUNCAO',
    'CONJ-S': 'CONJUNCAO',
    'CUR': 'MOEDA',
    'DAD': 'NUMERO',
    #'DAD': 'DAD',
    #'DAT': 'NUMERO',
    'DAT': 'DATA',
    'EC': 'PRT',  ############
    'EST': 'SUBSTANTIVO',
    #'EST': 'EST',  ############
    #'HOR': 'NUMERO',
    'HOR': 'HORA',
    #'IN': 'X',  ############
    'IN': 'INTERJEICAO',
    #'IN': 'INT',
    'KC': 'CONJUNCAO',
    'KS': 'CONJUNCAO',
    'N': 'SUBSTANTIVO',
    'NPRO': 'NPROPRIO',
    'NPROP': 'NPROPRIO',
    'NUM': 'NUMERO',
    'PCP': 'VERBO',
    'PDEN': 'ADVERBIO',
    #'PDEN': 'DENOTATIVA',  ############
    'PP': 'PREPOSICAO',
    'PREP': 'PREPOSICAO',
    'PRO-KS': 'PRONOME',
    'PRO-KS-REL': 'PRONOME',
    'PROADJ': 'PRONOME',
    'PRON-DET': 'PRONOME',
    'PRON-INDP': 'PRONOME',
    'PRON-PERS': 'PRONOME',
    'PROP': 'NPROPRIO',
    'PROPESS': 'PRONOME',
    'PROSUB': 'PRONOME',
    'PRP': 'PREPOSICAO',
    'PRP-': 'NPROPRIO',
    #'TEL': 'NUMERO',
    'TEL': 'TELEFONE',
    'V': 'VERBO',
    'V-FIN': 'VERBO',
    'V-GER': 'VERBO',
    'V-INF': 'VERBO',
    'V-PCP': 'VERBO',
    'VAUX': 'VERBO',
    'VP': 'VERBO',
}

translate = defaultdict(lambda: "__", translate)

##############################################################


DEBUG = False

if DEBUG:
    i=0
    testfrases = 20

filejson = 'wiki.json'
filelog = 'wiki.log'

base = mac_morpho.tagged_sents()
#base = floresta.tagged_sents()

print ("==========================CARREGANDO ARQUIVO\n...")
try:
    json_data=open(filejson).read()
    wiki = json.loads(json_data)
except IOError:
    wiki = []


print ("==========================PROCESSANDO\n...")
for sent in base:
    newsent=[]
    for word in sent:
        if len(word[1].split("|")) == 1:
            baseclass = word[1].upper()
            newclass = translate[baseclass]
            palavra = word[0].lower()
            newsent.append( (palavra, newclass) )
        else:
            baseclass = word[1].split('|')[0].upper()
            newclass = translate[baseclass]
            palavra = word[0].lower()
            newsent.append( (palavra, newclass) )
            #newsent.append((palavra, "CONTRACAO".decode("utf8")))

    wiki.append(newsent)
    if DEBUG:
        i=i+1
        if i>= testfrases:
            break



print ("==========================FINALIZANDO\n...")
totalfrases = str(len(wiki))
print ("Total de frases processadas: "+totalfrases)
with open(filelog, 'w') as outfile:
    json.dump("\nTotal de frases: "+totalfrases, outfile)

print ("==========================SALVANDO RESULTADO\n...")
with open(filejson, 'w') as outfile:
    json.dump(wiki, outfile)





if DEBUG:
    print ("==========================TESTANDO")
    from random import randint
    checksent = randint(0,testfrases)
    print ("FRASE:")
    frase = ""
    for w in base[checksent]:
        frase += w[0]+" "
    
    print (frase)
    print ("\nORIGINAL:")
    print (base[checksent])
    print ("\nWIKI:")
    print (wiki[checksent])

