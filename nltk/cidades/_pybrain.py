#coding: utf-8



import csv
import ast
import os
import numpy as np
import random, copy
import pickle

from math                           import sqrt
from sklearn.metrics                import mean_squared_error as MSE
from pybrain.datasets.supervised    import SupervisedDataSet as SDS
from pybrain.tools.shortcuts        import buildNetwork
from pybrain.supervised.trainers    import BackpropTrainer
from pybrain.tools.shortcuts        import buildNetwork

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





'''
class Generate:
	   
		def __init__(self,_x,_y):
				print("funcao Generacao .............. ")
				#print("ID,Adoption,Died,Euthanasia,Return_to_owner,Transfer")


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
'''



'''
from pybrain.datasets               import ClassificationDataSet
from pybrain.supervised.trainers    import BackpropTrainer
from pybrain.structure.modules      import SoftmaxLayer
'''


'''
insert = []
palavras = []
classificacoes = []
with open("cidadeslandia.txt", "r") as ins:
	for line in ins:
		line = line.strip()
		#insert.append([(line,"CIDADE")])
		palavras.append(line)
		classificacoes.append("CIDADE")


#prepara um banco de dados com as proporcoes dos arquivos de entrada _x e _y
traindata = ClassificationDataSet(len(palavras), 1, nb_classes=2)
testdata = ClassificationDataSet(len(palavras), 1, nb_classes=2)


#insere os exemplos
for p,c in zip(palavras,classificacoes):
		traindata.addSample(p,1)
		testdata.addSample(p,-1)
		#print(p+" : "+c)

traindata._convertToOneOfMany( )
fnn = buildNetwork( traindata.indim, 5, traindata.outdim, outclass=SoftmaxLayer )

trainer = BackpropTrainer( fnn, dataset=traindata, momentum=0.1, verbose=True, weightdecay=0.01)
fnn.activate( x )
'''