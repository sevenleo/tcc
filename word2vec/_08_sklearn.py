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
X_names = []
y = []



citys = []
animals = []
colors = []



for similar in w2v.most_similar("recife"):
	citys.append(similar[0])
	X_names.append(similar[0])

for similar in w2v.most_similar("cachorro"):
	animals.append(similar[0])
	X_names.append(similar[0])

for similar in w2v.most_similar("azul"):
	colors.append(similar[0])
	X_names.append(similar[0])



for city in citys:
	X.append(w2v[city].tolist())
	y.append(1)

for color in colors:
	X.append(w2v[color].tolist())
	y.append(-1)

for animal in animals:
	X.append(w2v[animal].tolist())
	y.append(-1)



#Shuffle lists
combined = list(zip(X, y))
random.shuffle(combined)
X,y = zip(*combined)




# Splitting the dataset into the Training set and Test set
#from sklearn.cross_validation import train_test_split
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

porcent=0.5
split = int(len(X)*porcent)

X_train = X[:split]
X_test = X[split:]

y_train = y[:split]
y_test = y[split:]

X_names_train = X_names[:split]
X_names_test = X_names[split:]



#SAVE_DATA
data = [X_train, X_test, y_train, y_test]
saveinfile(data,'train','data','predictions')


'''
#LOAD_DATA
data = loadfromfile('train','data','predictions')
X_train	= data[0]
X_test	= data[1]
y_train	= data[2]
y_test	= data[3]
'''



# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)



logs("Predicting")
total = len(y_pred)
ok = 0
fail = 0
for virtual,real in zip(y_pred,y_test):
	print(virtual,real)
	if real == virtual:
		ok = ok +1
	else:
		fail = fail + 1


logs("Percentual")
print("\nOk:",ok/total,"\nFail:",fail/total)



logs("Test new words")
newwords = ['recife','petrolina','rio de janeiro','niteroi','palmas','azul','amarelo','gato','vaca']
for word in newwords:
	try:
		print('\n' +word.upper())
		result = classifier.predict([w2v[word].tolist()])
		if result==1:
			print(result,'city')
		else:
			print(result,'not a city')

	except:
		print('not in vocab')
