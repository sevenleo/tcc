#coding: utf-8
import csv
import ast
import os
import numpy as np
import random, copy
import cPickle as pickle
import json

from math                           import sqrt
from sklearn.metrics                import mean_squared_error as MSE
from pybrain.datasets.supervised    import SupervisedDataSet as SDS
from pybrain.tools.shortcuts        import buildNetwork
from pybrain.supervised.trainers    import BackpropTrainer
from pybrain.tools.shortcuts        import buildNetwork

#from pybrain.tools.customxml        import NetworkWriter
#from pybrain.tools.customxml        import NetworkReader
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader

from pybrain.datasets               import ClassificationDataSet
from pybrain.utilities              import percentError
from pybrain.tools.shortcuts        import buildNetwork
from pybrain.supervised.trainers    import BackpropTrainer
from pybrain.structure.modules      import SoftmaxLayer
from pylab                          import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from scipy                          import diag, arange, meshgrid, where
from numpy.random                   import multivariate_normal

class Generate:
       
        def __init__(self,_x,_y):
                print("funcao Generacao .............. ")
                #print("ID,Adoption,Died,Euthanasia,Return_to_owner,Transfer")


        #http://pybrain.org/docs/tutorial/fnn.html
        def ReadTrainFile(self,_x,_y):
                print("Lendo matriz de treino .......")
                 #prepara um banco de dados com as proporcoes dos arquivos de entrada _x e _y
                TrainData = ClassificationDataSet(len(_x[0]), 1, nb_classes=5)

                #insere os exemplos
                i=0
                for line in _x:
                        TrainData.addSample(line, _y[i])
                        i+=1
                return TrainData



        def ReadTestFile(self,test_file,features):
                print("Lendo arquivo de teste ........")
                TestData = ClassificationDataSet(features, 1, nb_classes=5)               
                i=0
                test = open(test_file, 'r')
                for line in test:
                        nline = np.fromstring(line, dtype=int, sep=',')
                        TestData.addSample(nline, -1)
                        i+=1
                test.close()        
                return TestData



        def predict_class(self,_x,_y,test_file,epochs,steps):
                print("Iniciando funcao predict_class() .............")


                traindata = self.ReadTrainFile(_x,_y)
                #testdata = self.ReadTestFile( test_file, len(_x[0]) )
                
                print ("____________________________________________________________________________")
                print ("A matrix de treino tem ", len(traindata),"linhas de dados")
                print ("Dimensoes de Input e Output : ", traindata.indim, traindata.outdim)
                print ("____________________________________________________________________________\n")
                

                print("convertendo arquivos .................")

                traindata._convertToOneOfMany( )
                #testdata._convertToOneOfMany( )

                import os.path
                if os.path.exists('rede_animal.xml'):
                    print(" Carregando a rede de treinos do arquivo rede_animal.xml *************** ")
                    fnn = NetworkReader.readFrom('rede_animal.xml')
                else:
                    print(" Criando rede de treinos no arquivo rede_animal.xml *************** ")
                    fnn = buildNetwork( traindata.indim, 5, traindata.outdim, outclass=SoftmaxLayer )

                trainer = BackpropTrainer( fnn, dataset=traindata, momentum=0.1, verbose=True, weightdecay=0.01)

                print("Treinando .............")
                
                for i in range(epochs):
                        print("Treinando epoca ", i)
                        trainer.trainEpochs( steps )
                        NetworkWriter.writeToFile(fnn, 'rede_animal.xml')
                        print(" Rede salva em rede_animal.xml (Ok) ")

                print("Lendo arquivo de teste e classificando ..........")
                print("Gerando resultados em ANIMAL_OUTPUT.CSV ..........")
                output = open('animal_output.csv', 'wb')
                i=1
                output.write("ID,Adoption,Died,Euthanasia,Return_to_owner,Transfer\n")
                for line in open(test_file, 'r'):
                        x = ast.literal_eval(line)
                        output.write( "{},{},{},{},{},{} \n".format(i,fnn.activate( x )[0],fnn.activate( x )[1],fnn.activate( x )[2],fnn.activate( x )[3],fnn.activate( x )[4]) )
                        i=i+1   
                print("Concluido")

                





#test = "../data/shelter_animal/test.csv"
#train = "../data/shelter_animal/train.csv"
train = "train.csv"
test = "test.csv"

print("Deseja treinar [digite 0] ou calcular as probabilidades aleatóriamente [digite 1] ?")
treino = int( raw_input())

if treino !=1:
    print("Treino = train.csv\nTest = test.csv")
    print("Treinar por quantas epocas?")
    epocas = int( raw_input())
    print("E ciclos?")
    ciclos = int(raw_input())
    print("O Arquivo de saida estara em animal_output.csv")

print("Gerando csv detalhado (animal_train.csv) a partir do arquivo train.csv  ......................... ")
data = PrepareData(train)
f = open('animal_train.csv', 'wb')
for line in data.x:
    f.write((str(line)).split("[")[1].split("]")[0] + "\n")
f.close()

print("Gerando csv detalhado (animal_test.csv) a partir do arquivo test.csv ......................... ")
t = open('animal_test.csv', 'wb')
for line in data.PrepareTestFile(test):
    #f.write((str(line)).split("[")[1].split("]")[0] + "\n")
    t.write(str(line) + "\n")
t.close()

print("Trantando dados gerados ......................... ")
geracao = Generate(data.x,data.y)

if treino !=1:
    ## TRAIN PREDICT
    geracao.predict_class(data.x,data.y,"animal_test.csv",epocas,ciclos)

if treino ==1:
    ## RANDOM
    lines=0
    with open ('test.csv','rb') as f:
        for line in f:
            lines+=1

    print ("Linhas: ",lines-1)
    geracao.random(lines-1)


