#!/usr/bin/env python
# -*- coding: utf-8 -*- 

class postag:
    def __init__(self,entrada="Você esqueceu da entrada !",mac=False,floresta=False,wiki=True):

        #LINGUAGEM
        import nltk
        self.nltk = nltk
        self.lang = "portuguese"

        #SAIDA
        self.tela = "___TELA___\n"
        self.tabela = ""

        #CONTA TEMPO
        import time
        self.time = time
        self.start = self.time.time()

        #DATASETS
        self.mac=mac#False
        self.floresta=floresta#False
        self.wiki=wiki#True

        #LOAD ARQUIVOS
        import pickle
        self.saida("Dataset(s):")
        if self.mac==True:
            file="tag/tag_mac.obj"
            self.tag_mac = pickle.load(open(file, "r"))
            self.saida(file)
            pass
        if self.floresta==True:
            file="tag/tag_floresta.obj"
            self.tag_floresta = pickle.load(open(file, "r")) 
            self.saida(file)
            pass
        if self.wiki==True:
            try:
                file = "wiki.tag.obj"
                self.tag_wiki = pickle.load(open(file, "r"))
                print("TAG carregado atraves do arquivo: "+file)
            except:
                try:
                    file = "wiki.tag.objb"
                    self.tag_wiki = pickle.load(open(file, "rb"))
                    print("TAG carregado atraves do arquivo: "+file)
                except:
                    try:
                        filename = 'wiki.tag.json'
                        import json
                        with open(filename) as json_data:
                            self.tag_wiki = json.load(json_data)
                        print("TAG carregado atraves do arquivo: "+file)
                    except:
                        import sys
                        sys.exit("ERRO AO CARREGAR O ARQUIVO!!!!")
            #teste rapido
            #from nltk.corpus import mac_morpho
            #self.tag_wiki = nltk.UnigramTagger(mac_morpho.tagged_sents()[:100])
            self.saida(file)

        self.tag(entrada)
        #FIM DO CONSTRUTOR



    def __str__(self):

        return self.tela



    def saida(self,linha):

        self.tela += str(linha)+"\n"



    def salvatabela(self,conteudo):

        self.tabela = conteudo



    def tokenize(self,frase):
        tokens=[]
        for word in self.nltk.word_tokenize(frase, self.lang):
                #tokens.append(word.decode("utf-8"))
                tokens.append(word)
        return tokens
        


    def relevant_words(self, frases):
        frases_t = self.nltk.sent_tokenize(frases, self.lang)
        stopwords = [] 
        palavras = []
        for frase in frases_t:
            for palavra in self.tokenize(frase):
                if palavra.lower() in stopwords:
                    continue
                palavras.append(palavra)
        return palavras



    def tag_word(self, word):
        result = ["","",""]
        if self.mac==True:
            result[0] = self.tag_mac.tag([word])
        if self.floresta==True:
            result[1] = self.tag_floresta.tag([word])
        if self.wiki==True:
            result[2] = self.tag_wiki.tag([word])
        return result
  


    def tag_text(self, text):
        words = self.relevant_words(text)
        result = ["","",""]
        if self.mac==True:
            result[0] = self.tag_mac.tag(words)
        if self.floresta==True:
            result[1] = self.tag_floresta.tag(words)
        if self.wiki==True:
            result[2] = self.tag_wiki.tag(words)
        return result



    def tag(self,entrada):

        import pickle, nltk
        from terminaltables import AsciiTable

        self.saida("iniciando analise...")
        self.saida("Entrada")
        self.saida(entrada)


        #TOKENIZAR
        tokens = self.tokenize(entrada)
        self.saida("Quantidade de Tokens : ")
        self.saida(len(tokens))                 
        self.saida("Tokens relevantes:")
        self.saida(self.relevant_words(entrada))

        #ANALISE DA PRIMEIRA PALAVRA
        palavra1 = self.tag_word(tokens[0])
        self.saida("1a palavra:")
        self.saida(palavra1)

        #ANALISE DO TEXTO
        tagged = self.tag_text(entrada)

        self.saida("Classificacao:")
        self.saida(str(tagged[2]))

        #TABELA DE EXIBICAO
        table_data = []
        table_data.append(["Palavra:","(mac_morpho)","(floresta)","(wiki_pessoal)"])

        for w in range(0,len(tokens)):
            linha = [tokens[w].upper()]
            if self.mac:
                linha.append(str(tagged[0][w][1]).lower())
            else:
                linha.append("")  
            if self.floresta:
                linha.append(str(tagged[1][w][1]).lower())
            else:
                linha.append("")  
            if self.wiki:
                linha.append(str(tagged[2][w][1]).lower())
            else:
                linha.append("")  
            table_data.append(linha)


        table = AsciiTable(table_data)
        self.salvatabela(table.table)
        #CONTAGEM DE TEMPO
        end = self.time.time()
        self.saida("\nTempo de execucao: "+str(end - self.start)+" seg")







###################################################

import os

DEBUG = True
if DEBUG:
    dataset="DEBUG"
else:
    dataset = raw_input(
        "Escolha o dataset:\n \
        * [MAC]_morpho\n \
        * [FLOR]esta\n \
        * Ambos [2]\n \
        * [WIKI]\t[default]\n \
        * TODOS [3]\n \
    ")

if dataset.lower() == "mac":
    mac=True
elif dataset.lower() == "wiki":
    wiki=True
elif dataset.lower() == "flor":
    floresta=True
elif dataset=="2":
    mac=True
    floresta=True
elif dataset=="3":
    mac=True
    floresta=True
    wiki=True
else:
    mac=False
    floresta=False
    wiki=True



while (True):
    if DEBUG:
        entrada = "Oi amigos, todos vocês irão viajar na viagem da semana que vem ?"
        print("(Modo Debug)Entrada:")
        print(entrada)
    else:
        entrada = raw_input("Digite o texto que deseja classificar:\n").lower()
        if entrada=="":
            break
        if entrada.startswith("---"):
            entrada=entrada.split("---")[1]
            os.system("clear")

    #entrada = entrada.decode("utf-8")
    analise = postag(entrada,mac,floresta,wiki)  
    print(analise)
    print(analise.tabela)
    if DEBUG:
        break