#https://radimrehurek.com/gensim/models/word2vec.html
#https://codesachin.wordpress.com/2015/10/09/generating-a-word2vec-model-from-a-block-of-text-using-gensim-python/
#https://radimrehurek.com/gensim/models/doc2vec.html



from _00_functions import *





#IMPORT
logs("IMPORT")
#import nltk
import glob
import logging
from multiprocessing import cpu_count


try:
	lang=str(sys.argv[1])
	file = lang
except:
	pass
	lang='pt'
	file = 'corpus.clean.pt'

print('lang')
print(lang)
print('file')
print(file)

level=1
erros = 0

stopw = create_stopwords()


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim.models import Word2Vec


try:
	#LOAD FILES
	try:
		loadfilename = 'W2V'+'/'+file+'.model'
		logs("LOAD FILE (model)",loadfilename)
		w2v = Word2Vec.load(loadfilename)
		print("FILE LOADED")
	except:
		print(file+".model FILE NOT EXIST")
		w2v = loadfromfile('W2V',file,'W2V')
except:
	erros += 1
	print("**** ERRO = {}".format(erros))
	print(file+".objb FILE NOT EXIST")
	print("FILE CANNOT BE LOADED")
	#CREATE W2V
	logs("CREATE W2V",file)
	
	from gensim.models.word2vec import LineSentence,PathLineSentences
	##sentences = LineSentence('myfile.txt')
	##sentences = LineSentence('compressed_text.txt.bz2')
	##sentences = LineSentence('compressed_text.txt.gz')


	##all files in language
#	sentences = LineSentence("texts/"+lang)
#	files = sorted(glob.glob("texts/*."+lang))
#	print(files)
#	for _file in files:
#		print("\n\nLoading: ",_file,"\n\n")
#		sentences = sentences+LineSentence(_file)
#		try:
#			print('Somando')
#		except:
#			#sentences = sentences+LineSentence(_file)
#			print('Criando')

	#all files
	sentences = PathLineSentences("texts/pt")


	##especific namefile
	#	sentences = ""
	#	files = sorted(glob.glob("texts/*"+file+"*"))
	#	for file in files: 
	#		sentences = sentences + LineSentence('texts/'+file)
	
	##especific type
	#	sentences = ""
	#	files = sorted(glob.glob("texts/*.txt*"))
	#	for file in files: 
	#		sentences = sentences + LineSentence('texts/'+file)


	#create model
	if level==0:
		w2v = Word2Vec(sentences)

	elif level==1:
		min_word_count = 0
		num_workers = cpu_count()
		w2v = Word2Vec(
		    workers=num_workers,
		    min_count=min_word_count
		)
		w2v.build_vocab(sentences)
		w2v.train(sentences,total_examples=w2v.corpus_count, epochs=w2v.iter)

	else:

		#https://github.com/llSourcell/word_vectors_game_of_thrones-LIVE/blob/master/Thrones2Vec.ipynb
		#ONCE we have vectors
		#step 3 - build model
		#3 main tasks that vectors help with
		#DISTANCE, SIMILARITY, RANKING

		# Dimensionality of the resulting word vectors.
		#more dimensions, more computationally expensive to train
		#but also more accurate
		#more dimensions = more generalized
		num_features = 300
		# Minimum word count threshold.
		min_word_count = 3

		# Number of threads to run in parallel.
		#more workers, faster we train
		num_workers = cpu_count()

		# Context window length.
		context_size = 7

		# Downsample setting for frequent words.
		#0 - 1e-5 is good for this
		downsampling = 1e-3

		# Seed for the RNG, to make the results reproducible.
		#random number generator
		#deterministic, good for debugging
		seed = 1

		w2v = Word2Vec(
		    sg=1,
		    seed=seed,
		    workers=num_workers,
		    size=num_features,
		    min_count=min_word_count,
		    window=context_size,
		    sample=downsampling
		)


		w2v.build_vocab(sentences)
		w2v.train(sentences,total_examples=w2v.corpus_count, epochs=w2v.iter)





	#SAVE FILES
	try:
		savefilename = 'W2V'+'/'+file+'.model'
		logs("SAVE FILE (model)",savefilename)
		w2v.save(savefilename)
		print("FILE SAVED")
	except:
		erros += 1
		print("**** ERRO = {}".format(erros))
		print(file+".model FILE CANNOT BE SAVED")
		saveinfile(w2v,W2V,file,W2V)

size(w2v)


#USES
#newwords = ['CIDADE','ESTADO','PRESIDENTE','casal','goiania','recife']
#for newword in newwords:
#	predicts,similares,erros = checkinmodel(w2v,newword,erros)

folder = "texts/"+lang+"/"
for _file in sorted(glob.glob(folder+"*")):
	newword = _file.replace(folder,"").replace(".wiki","")
	predicts,similares,erros = checkinmodel(w2v,newword,erros)
predicts,similares,erros = checkinmodel(w2v,'cantora',erros)
predicts,similares,erros = checkinmodel(w2v,'jogador',erros)

logs('END')
print("Files in:",lang,"\n")
folder = "texts/"+lang+"/"
for _file in sorted(glob.glob(folder+"*")):
	print(_file.replace("texts/"+lang,""))
print('cantora')
print('jogador')
#
#
#print(w2v.predict_output_word(['Neymar','anos']))
#print(w2v.most_similar(['Neymar','anos'], topn=5))