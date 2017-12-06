#!/usr/bin/env python
# -*- coding: utf-8 -*- 



from _00_functions import *




class similar_wiki:
    def __init__(self,entrada="Você esqueceu da entrada !",model='wikipedia'):
        import nltk
        from terminaltables import AsciiTable
        self.AsciiTable = AsciiTable
        self.nltk = nltk
        self.lang = "portuguese"
        self.tela = ""
        self.tabela = ""
        self.generate_similar(entrada)


    def __str__(self):
        return self.tela    



    def saida(self,linha=""):
        self.tela += str(linha)+"\n"



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



    def salvatabela(self,conteudo):
        self.tabela = conteudo



    def similar_from_wiki(self,words,file='wikipedia'):
        erros   = 0

        #LOAD FILES
        try:
            loadfilename = 'W2V'+'/'+file+'.model'
            logs("LOAD FILE (model)",loadfilename)
            w2v = Word2Vec.load(loadfilename)
            print("FILE LOADED")
        except:
            print(file+".model FILE NOT EXIST")
            w2v = loadfromfile('W2V',file,'W2V')
            exit()


        similares =[]
        for word in words:
            predict,similar,error = checkinmodel_without_prints(w2v,word,erros)
            if predict == []:
                predict.append([word,1.0])
            if similar == []:
                similar.append([word,1.0])
            similares.append(similar[0][0])

        return similares




    def generate_similar(self,entrada):

        self.saida("Texto de entrada:")
        self.saida(entrada)


        #TOKENIZAR
        tokens = self.tokenize(entrada)
        self.saida()
        self.saida("Quantidade de Tokens : ")
        self.saida(len(tokens))

        #TOKENS RELEVANTES                 
        #self.saida("Tokens relevantes:")
        #self.saida(self.relevant_words(entrada))

        #ANALISE DA PRIMEIRA PALAVRA
        #palavra1 = self.similar_from_wiki(tokens[0])
        #self.saida("1a palavra:")
        #self.saida(palavra1)

        #CRIAR TEXTO SIMILAR
        texto_similar = []
        
        #PALAVRA POR PALAVRA
        #for token in tokens:
        #    similar = self.similar_from_wiki(token)
        #    texto_similar.append(similar)
        
        #TODOS OS TOKENS DE UMA VEZ
        texto_similar = self.similar_from_wiki(tokens)

        #TABELA DE EXIBICAO
        table_data = []
        table_data.append(["ORIGINAL:","SIMILAR"])
        for word,similar in zip(tokens,texto_similar):
            linha = [word,similar] 
            table_data.append(linha)
        table = self.AsciiTable(table_data)
        self.salvatabela(table.table)






if __name__ == "__main__":

    DEBUG = True
    if DEBUG:
        pass
    else:
        pass


    while (True):
        if DEBUG:
            entrada = "Oi amigos, todos vocês irão viajar na viagem da semana que vem para florianopolis, anopolis, rolandia ou Imagilandia ?"
            print("(Debug)")
        else:
            #entrada = raw_input("Digite o texto que deseja simular:\n").lower()        #python2
            entrada = input("Digite o texto que deseja simular:\n").lower()             #python3
            if entrada=="":
                break
            if entrada.startswith("---"):
                entrada=entrada.split("---")[1]
                os.system("clear")

        #entrada = entrada.decode("utf-8")
        analise = similar_wiki(entrada,'wikipedia')
        print("\n___TELA___\n")  
        print(analise.tela)
        print("\n___TABELA___\n")  
        print(analise.tabela)
        if DEBUG:
            break
    