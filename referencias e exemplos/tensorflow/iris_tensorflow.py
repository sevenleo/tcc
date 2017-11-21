
#Depois de apanhar um pouco do código que tinhamos visto aquele dia. 
#Desisti e procurei outro, eis que no próprio site do tensorflow tem exemplo usando a iris.
#
#https://www.tensorflow.org/get_started/tflearn
#
#
#Mas ele usa python2 dá uns erros de import e execucao no python3 mas no final roda.
#
#Se quiserem testar um exemplo com um código mais redondo tentem este.
#https://gist.github.com/anonymous/e33e0c7f1b0a45a7da58dbbbf2f0b913


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

'''
#COMPLICADO IMPORTAR ISSO NO PYTHON3, MAS FACIL BAIXAR OS ARQUIVOS MANUALMENTE
import sys
import urllib.request
import urllib
'''

import tensorflow as tf
import random
import numpy as np
import os


'''
#In TensorFlow 0.12+, per this issue, you can now control logging via the environmental 
variable called TF_CPP_MIN_LOG_LEVEL; it defaults to 0 (all logs shown), but can be set to 
1 to filter out INFO logs, 
2 to additionally filter out WARNING logs, 
3 to additionally filter out ERROR logs. 
See the following generic OS example using Python:
'''
#### ERA PRA TENTAR SUPRIMIR OS WARNINGS PELO JEITO NAO FUNCIONOU ...
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'	# or any {'0', '1', '2'}



############
# #BAIXAR ESTES DOIS ARQUIVOS E COLOCAR NA MESMA PASTA
############


# Data sets
IRIS_TRAINING = "iris_training.csv"
IRIS_TRAINING_URL = "http://download.tensorflow.org/data/iris_training.csv"

IRIS_TEST = "iris_test.csv"
IRIS_TEST_URL = "http://download.tensorflow.org/data/iris_test.csv"

def main():
	# If the training and test sets aren't stored locally, download them.

	'''
	if not os.path.exists(IRIS_TRAINING):
		raw = urllib.request.urlopen(IRIS_TRAINING_URL).read()
		with open(IRIS_TRAINING, "wb") as f:
			f.write(raw)

	if not os.path.exists(IRIS_TEST):
		raw = urllib.request.urlopen(IRIS_TEST_URL).read()
		with open(IRIS_TEST, "wb") as f:
			f.write(raw)

	'''


	# Load datasets.
	training_set = tf.contrib.learn.datasets.base.load_csv_with_header(
			filename=IRIS_TRAINING,
			target_dtype=np.int,
			features_dtype=np.float32)

	test_set = tf.contrib.learn.datasets.base.load_csv_with_header(
			filename=IRIS_TEST,
			target_dtype=np.int,
			features_dtype=np.float32)

	# Specify that all features have real-value data
	feature_columns = [tf.contrib.layers.real_valued_column("", dimension=4)]

	# Build 3 layer DNN with 10, 20, 10 units respectively.
	classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
																							hidden_units=[10, 20, 10],
																							n_classes=3,
																							model_dir="/tmp/iris_model")
	# Define the training inputs
	def get_train_inputs():
		x = tf.constant(training_set.data)
		y = tf.constant(training_set.target)

		return x, y

	# Fit model.
	classifier.fit(input_fn=get_train_inputs, steps=2000)

	# Define the test inputs
	def get_test_inputs():
		x = tf.constant(test_set.data)
		y = tf.constant(test_set.target)

		return x, y


	# Evaluate accuracy.
	accuracy_score = classifier.evaluate(input_fn=get_test_inputs, steps=1)["accuracy"]

	print("\nTest Accuracy: {0:f}\n".format(accuracy_score))

	# Classify two new flower samples.
	def new_samples():
			return np.array([
                [6.4, 3.2, 4.5, 1.5],
                [5.8, 3.1, 5.0, 1.7],
                np.random.uniform(0, 10, 4),
                np.random.uniform(0, 10, 4),
                np.random.uniform(0, 10, 4),
                np.random.uniform(0, 10, 4),
                np.random.uniform(0, 10, 4)
                 ],dtype=np.float32)


	predictions = list(classifier.predict(input_fn=new_samples))


	print(
			"New Samples, Class Predictions:		{}\n"
			.format(predictions))



if __name__ == "__main__":
		main()
