import nltk
nltk.download('averaged_perceptron_tagger')

sentence = "As seis da manha desta terca-feira, Arthur nao se sentia bem. Porem ainda eram 6 da manha";
#sentence = """At eight o'clock on Thursday morning
#... Arthur didn't feel very good."""
tokens = nltk.word_tokenize(sentence)
print ("tokens")
print (tokens)
# ['At', 'eight', "o'clock", 'on', 'Thursday', 'morning',
# 'Arthur', 'did', "n't", 'feel', 'very', 'good', '.']
tagged = nltk.pos_tag(tokens)
print("\n\ntagged")
print(tagged[0:6])
# [('At', 'IN'), ('eight', 'CD'), ("o'clock", 'JJ'), ('on', 'IN'),
# ('Thursday', 'NNP'), ('morning', 'NN')]
tokenizer=nltk.data.load('tokenizers/punkt/portuguese.pickle')
frases = tokenizer.tokenize(sentence);
for frase in frases:
	print("[Frase]:  "+frase)
