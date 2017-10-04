#!/usr/bin/env python
# -*- coding: latin-1 -*- 

#import unidecode
#unaccented_string = unidecode.unidecode(txt)
import pickle
import nltk
from nltk.corpus import mac_morpho, stopwords


#__________________________________________________________________________

definitions_mac = {
    'ART': 'artigo',
    'ADJ': 'adjetivo',
    'N': 'nome',
    'NPROP': 'nome proprio',
    'NUM': 'numeral',
    'PROADJ': 'pronome adjetivo',
    'PROSUB': 'pronome substantivo',
    'PROPESS': 'pronome pessoal',
    'PRO-KS': 'pronome conectivo subordinativo',
    'PRO-KS-REL': 'pronome conectivo subordinativo relativo',
    'ADV': 'adverbio',
    'ADV-KS': 'adverbio conectivo subordinativo',
    'ADV-KS-REL': 'adverbio relativo subordinativo',
    'KC': 'conjuncao cordenativa',
    'KS': 'conjuncao subordinativa',
    'PREP': 'preposicao',
    'IN': 'interjeicao',
    'V': 'verbo',
    'VAUX': 'verbo auxiliar',
    'PCP': 'participio',
    'PDEN': 'palavra denotativa',
    'CUR': 'simbolo de moeda corrente',
    '.' :   'ponto',

    #devo retirar isso daqui e adicionar como stopword
    #'.' :   'ponto',
    #,',' :   'virgula',
    #'!' :   'exclamacao',
    #'?' :   'interrogacao'
}

complement_mac = {
    'EST': 'estrangeirismo',
    'AP': 'apostos',
    'DAD': 'dados',
    'TEL': 'telefone',
    'DAT': 'data',
    'HOR': 'hora',

}

connectors_mac = {
    '|': 'complemento',
    '|+': 'contracoes e eclises',
    '|!': 'mesoclise',
}



definitions_floresta = {
    'n': "NOUN",
    'num': "NUM",
    'v-fin': "VERB",
    'v-inf': "VERB",
    'v-ger': "VERB",
    'v-pcp': "VERB",
    'pron-det': "PRON",
    'pron-indp': "PRON",
    'pron-pers': "PRON",
    'art': "DET",
    'adv': "ADV",
    'conj-s': "CONJ",
    'conj-c': "CONJ",
    'conj-p': "CONJ",
    'adj': "ADJ",
    'ec': "PRT",
    'pp': "ADP",
    'prp': "ADP",
    'prop': "NOUN",
    'pro-ks-rel': "PRON",
    'proadj': "PRON",
    'prep': "ADP",
    'nprop': "NOUN",
    'vaux': "VERB",
    'propess': "PRON",
    'v': "VERB",
    'vp': "VERB",
    'in': "X",
    'prp-': "ADP",
    'adv-ks': "ADV",
    'dad': "NUM",
    'prosub': "PRON",
    'tel': "NUM",
    'ap': "NUM",
    'est': "NOUN",
    'cur': "X",
    'pcp': "VERB",
    'pro-ks': "PRON",
    'hor': "NUM",
    'pden': "ADV",
    'dat': "NUM",
    'kc': "ADP",
    'ks': "ADP",
    'adv-ks-rel': "ADV",
    'npro': "NOUN",
    '.' : 'ponto',

    'N|AP' :'NUM',
    'N|DAD' :'NUM',
    'N|DAT' :'NUM',
    'N|HOR' :'NUM',
    'N|TEL' :'NUM'
}



#__________________________________________________________________________


lang = 'portuguese'
#train = mac_morpho.tagged_sents()[100:]
#test = mac_morpho.tagged_sents()[:100]


#__________________________________________________________________________

dataset = raw_input("Escolha o dataset:\n* [MAC]_morpho\n* [FLOR]esta\n* AMBOS [2]\n* Test\t[default]\n")
if dataset.lower() == "mac":
    mac=True
    floresta=False
elif dataset.lower() == "flor":
    mac=False
    floresta=True
elif dataset=="3" or dataset=="2":
    mac=True
    floresta=True
else:
    mac=False
    floresta=False




#LOAD MAC_MORPHO TRAINED FILE
if mac==True:
    file_tag3_mac = open('tag3_mac.obj', 'r') 
    tag3_mac = pickle.load(file_tag3_mac) 




#LOAD FLORESTA TRAINED FILE
if floresta==True:
    file_tag3_floresta = open('tag3_floresta.obj', 'r') 
    tag3_floresta = pickle.load(file_tag3_floresta) 


#LOAD TESTE FILE
if (floresta==False and mac==False) or (floresta==True and mac==True):
    file_tag3_test = open('tag3_test.obj', 'r') 
    tag3_test = pickle.load(file_tag3_test) 	


#__________________________________________________________________________



#FUNCOES DE ANALISE
def relevant_words(text, RemoveStopwords = False):
    sentences = nltk.sent_tokenize(text, lang)
    words = []
    for sent in sentences:
        for word in nltk.word_tokenize(sent, lang):
            words.append(word)

    sws = stopwords.words(lang)
    if RemoveStopwords:
        relevant = []
        for word in words:
            if word not in sws:
                relevant.append(word)
    else:
        relevant = words
    return relevant



def tag_text(text, RemoveStopwords = False):
    words = relevant_words(text,RemoveStopwords)
    if mac==True:
        result = tag3_mac.tag(words)
    elif floresta==True:
        result = tag3_floresta.tag(words)
    else:
    	result = tag3_test.tag(words)
    return result
 


def tag_word(word):
    if mac==True:
        result = tag3_mac.tag([word])
    elif floresta==True:
        result = tag3_floresta.tag([word])
    else:
    	result = tag3_test.tag([word])
    return result

#__________________________________________________________________________



#FRASE
pensamento_original="Pensamento e pensar são, respectivamente, uma forma de processo mental ou faculdade do sistema mental.[1] Pensar permite aos seres modelarem sua percepção do mundo ao redor de si, e com isso lidar com ele de uma forma efetiva e de acordo com suas metas, planos e desejos. Palavras que se referem a conceitos e processos similares incluem cognição, senciência, consciência, ideia, e imaginação. O pensamento é considerado a expressão mais 'palpável' do espírito humano, pois através de imagens e ideias revela justamente a vontade deste. O pensamento é fundamental no processo de aprendizagem (vide Piaget). O pensamento é construto e construtivo do conhecimento. O principal veículo do processo de conscientização é o pensamento. A atividade de pensar confere ao homem 'asas' para mover-se no mundo e 'raízes' para aprofundar-se na realidade. Etimologicamente, pensar significa avaliar o peso de alguma coisa. Em sentido amplo, podemos dizer que o pensamento tem como missão tornar-se avaliador da realidade."
#  https://www.miniwebtool.com/remove-accent/
pensamento_sem_acentos="Pensamento e pensar sao, respectivamente, uma forma de processo mental ou faculdade do sistema mental.[1] Pensar permite aos seres modelarem sua percepcao do mundo ao redor de si, e com isso lidar com ele de uma forma efetiva e de acordo com suas metas, planos e desejos. Palavras que se referem a conceitos e processos similares incluem cognicao, senciencia, consciencia, ideia, e imaginacao. O pensamento e considerado a expressao mais 'palpavel' do espirito humano, pois atraves de imagens e ideias revela justamente a vontade deste. O pensamento e fundamental no processo de aprendizagem (vide Piaget). O pensamento e construto e construtivo do conhecimento. O principal veiculo do processo de conscientizacao e o pensamento. A atividade de pensar confere ao homem 'asas' para mover-se no mundo e 'raizes' para aprofundar-se na realidade. Etimologicamente, pensar significa avaliar o peso de alguma coisa. Em sentido amplo, podemos dizer que o pensamento tem como missao tornar-se avaliador da realidade."
pensamento="Pensamento e pensar sao respectivamente uma forma de processo mental ou faculdade do sistema mental. Pensar permite aos seres modelarem sua percepcao do mundo ao redor de si e com isso lidar com ele de uma forma efetiva e de acordo com suas metas planos e desejos. Palavras que se referem a conceitos e processos similares incluem cognicao senciencia consciencia ideia e imaginacao. O pensamento e considerado a expressao mais palpavel do espirito humano pois atraves de imagens e ideias revela justamente a vontade deste. O pensamento e fundamental no processo de aprendizagem. O pensamento e construto e construtivo do conhecimento. O principal veiculo do processo de conscientizacao e o pensamento. A atividade de pensar confere ao homem asas para mover-se no mundo e raizes para aprofundar-se na realidade. Etimologicamente pensar significa avaliar o peso de alguma coisa. Em sentido amplo podemos dizer que o pensamento tem como missao tornar-se avaliador da realidade."










print("Exemplo:\n"+pensamento+"\n")


while (mac==True and floresta==False):
    print("___________________________________________")
    entrada = raw_input("[mac]Digite o texto que deseja classificar:\n")

    if entrada=="":
        break
    tagged = tag_text(entrada.decode('latin-1'))



    #CLASSIFICADAS
    print("\n\n* Palavra / Classificacao: *")
    for t in tagged:
        if t[1] != "unk":
            classification = t[1]
            if "+" in t[1]: classification = t[1].split("+")[1]
            if "|" in t[1]: classification = t[1].split("|")[1]
            if "#" in t[1]: classification = t[1].split("#")[0]
            
            if classification in definitions_mac:
                classification = definitions_mac[classification]                
            else:
                classification = "Simbolo ou pontuacao"

            print(t[0].upper()+"  ("+ classification+")\n")


    #CLASSIFICACAO DESCONHECIDA
    print("\n\n** Palavras nao classificadas: **")
    for t in tagged:
        if t[1] == "unk":
            print(t[0])





while (floresta==True and mac==False):
    print("___________________________________________")
    entrada = raw_input("[floresta]Digite o texto que deseja classificar:\n")
    if entrada=="":
        break
    tagged = tag_text(entrada)



    #CLASSIFICADAS
    print("\n\n* Palavra / Classificacao: *")
    for t in tagged:
        if t[1] != "unk":
            
            classification = t[1]
            if "+" in t[1]: classification = t[1].split("+")[1]
            if "|" in t[1]: classification = t[1].split("|")[1]
            if "#" in t[1]: classification = t[1].split("#")[0]
            
            if classification in definitions_floresta:
                classification = definitions_floresta[classification]                
            else:
                classification = "Simbolo ou pontuacao"

            print(t[0].upper()+"  ("+ classification+")\n")

 


    #CLASSIFICACAO DESCONHECIDA
    print("\n\n** Palavras nao classificadas: **")
    for t in tagged:
        if t[1] == "unk":
            print(t[0])





while (floresta==True and mac==True):
    print("___________________________________________")
    entrada = raw_input("[ambos]Digite o texto que deseja classificar:\n")
    if entrada=="":
        break
    
    mac=True
    floresta=False
    tagged_m = tag_text(entrada)
    
    m_c=0
    m_nc=0

    for t in tagged_m:
        if t[1] != "unk":
            m_c = m_c + 1
        else:
            m_nc = m_nc + 1
            
    print("\nmac -> classificados : "+str(m_c))        
    print("\nmac -> n-classificados : "+str(m_nc))
                        




    mac=False
    floresta=True
    tagged_f = tag_text(entrada)

    f_c=0
    f_nc=0

    for t in tagged_f:
        if t[1] != "unk":
            f_c = f_c + 1
        else:
            f_nc = f_nc + 1
            
    print("\nflr -> classificados : "+str(f_c))        
    print("\nflr -> n-classificados : "+str(f_nc))

    

    mac=False
    floresta=False
    tagged_t = tag_text(entrada)

    t_c=0
    t_nc=0

    for t in tagged_t:
        if t[1] != "unk":
            t_c = t_c + 1
        else:
            t_nc = t_nc + 1
            
    print("\ntst -> classificados : "+str(t_c))        
    print("\ntst -> n-classificados : "+str(t_nc))

    

    mac=True
    floresta=True




while (mac==False and floresta==False):
    #print("____EX ENCODE DECODE USANDO AS STOPWORDS_______")
    #print( stopwords.words(lang)[36:40] )

    print("________________________________________________")
    entrada = raw_input("[test]Digite o texto que deseja classificar:\n")

    if entrada=="":
        break
    
    #print("\n")
    #print("\n         ->")
    #print(entrada)
    
    #print("\n ISO 8859-1 ->")
    #print(entrada.decode('ISO 8859-1'))

    #print("\n latin-1 ->")
    #print(entrada.decode('latin-1'))
    #print("\n utf-8 ->")
    #print(entrada.decode('utf-8'))
    #print("\n       ->  latin-1 ")
    #print(entrada.encode('latin-1'))
    #print("\n       ->  utf-8")
    #print(entrada.encode('utf-8'))
    #print("\n latin-1 -> utf-8")
    #print(entrada.decode('latin-1').encode('utf-8'))
    #print("\n latin-1 -> latin-1")
    #print(entrada.decode('latin-1').encode('latin-1'))
    #print("\n utf-8   -> latin-1")
    #print(entrada.decode('latin-1').encode('utf-8'))



    tagged = tag_text(entrada)



    #CLASSIFICADAS
    print("\n\n* Palavra / Classificacao: *")
    for t in tagged:
        if t[1] != "unk":
            classification = t[1]
            if "+" in t[1]: classification = t[1].split("+")[1]
            if "|" in t[1]: classification = t[1].split("|")[1]
            if "#" in t[1]: classification = t[1].split("#")[0]
            
            if classification in definitions_mac:
                classification = definitions_mac[classification]                
            #else:
            #    classification = "Simbolo ou pontuacao"

            print(t[0].upper()+"  ("+ classification+")\n")


    #CLASSIFICACAO DESCONHECIDA
    print("\n\n** Palavras nao classificadas: **")
    for t in tagged:
        if t[1] == "unk":
            print(t[0])

	