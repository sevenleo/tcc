import gensim
import numpy as np
import os
from datetime import datetime

# Número de predições consideradas
TOPN = 10

def load_word2vec_model(model_path):
    """Carrega o modelo Word2Vec do arquivo especificado."""
    return gensim.models.Word2Vec.load(model_path)

def load_vocabulary(vocab_path):
    """Carrega o vocabulário do arquivo especificado com codificação UTF-8."""
    with open(vocab_path, 'r', encoding='utf-8') as file:
        return set(word.strip() for word in file.readlines())

def load_analogies(analogy_file):
    """Carrega o conjunto de analogias do arquivo especificado."""
    analogies = []
    with open(analogy_file, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                analogies.append(parts)
    return analogies

def evaluate_analogies(model, analogies, topn=TOPN):
    """Avalia a acurácia do modelo Word2Vec usando um conjunto de analogias e salva os resultados em um arquivo."""
    total_accuracy = 0
    total_analogies = len(analogies)
    results = []

    for base, target in analogies:
        if base in model.wv:
            # Calcula as palavras mais similares à palavra base
            result = model.wv.most_similar(base, topn=topn)
            
            similarity_sum = 0
            for word in result:
                similarity = model.wv.similarity(target, word)
                similarity_sum += similarity
            similarity_avg = similarity_sum/topn

            print(base,target,result,similarity_sum,similarity_avg)




    return overall_accuracy

def main():
    model_path = 'modelo/word2vec.model'
    vocab_path = 'modelo/vocabulary.txt'
    analogy_file = 'analogias_duplas.txt'  # Substitua pelo caminho para seu arquivo de analogias

    # Carregar o modelo e o vocabulário
    model = load_word2vec_model(model_path)
    vocabulary = load_vocabulary(vocab_path)

    # Carregar e filtrar as analogias
    analogies = load_analogies(analogy_file)
    analogies = [a for a in analogies if all(word in vocabulary for word in a)]

    # Avaliar a acurácia e salvar resultados
    accuracy = evaluate_analogies(model, analogies)
    print(f'\nAcurácia do modelo: {accuracy:.2%}')

if __name__ == "__main__":
    main()
