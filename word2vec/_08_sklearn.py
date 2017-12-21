from _00_functions import *


try:
	file = str(sys.argv[1])
except:
	file = 'wikipedia'

erros = 0


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


X = []
y = []

citys = []
animals = []
colors = []

for similar in w2v.most_similar("recife"):
	citys.append(similar[0])

for similar in w2v.most_similar("cachorro"):
	animals.append(similar[0])

for similar in w2v.most_similar("azul"):
	colors.append(similar[0])

for city in citys:
	X.append(w2v[city].tolist())
	y.append(1)

for color in colors:
	X.append(w2v[color].tolist())
	y.append(-1)

for animal in animals:
	X.append(w2v[animal].tolist())
	y.append(-1)




# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)


#save
data = [X_train, X_test, y_train, y_test]
saveinfile(data,'train','data','predictions')




##load
#data = loadfromfile('train','data','predictions')
#X_train	= data[0]
#X_test	= data[1]
#y_train	= data[2]
#y_test	= data[3]


print (X_train)


# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
#from sklearn.metrics import confusion_matrix
#cm = confusion_matrix(y_test, y_pred)


#from sklearn.cross_validation import train_test_split
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)
#TypeError: Expected sequence or array-like, got <class 'gensim.models.word2vec.Word2Vec'>