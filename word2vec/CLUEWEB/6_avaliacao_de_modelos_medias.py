import gensim
import numpy as np
import os
from datetime import datetime

# Número de predições consideradas
TOPN = 10

def load_word2vec_model(model_path):
    """Carrega o modelo Word2Vec do arquivo especificado."""
    try:
        return gensim.models.Word2Vec.load(model_path)
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        raise

def load_vocabulary(vocab_path):
    """Carrega o vocabulário do arquivo especificado com codificação UTF-8."""
    try:
        with open(vocab_path, 'r', encoding='utf-8') as file:
            return set(word.strip() for word in file.readlines())
    except Exception as e:
        print(f"Erro ao carregar o vocabulário: {e}")
        raise

def load_analogies(analogy_file):
    """Carrega o conjunto de analogias do arquivo especificado."""
    analogies = []
    try:
        with open(analogy_file, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2:
                    analogies.append(parts)
    except Exception as e:
        print(f"Erro ao carregar as analogias: {e}")
        raise
    return analogies

def format_table_header():
    """Gera o cabeçalho da tabela."""
    header = "+----------------+----------------+--------------------+--------------------+"
    line = "+----------------+----------------+--------------------+--------------------+"
    return header, line

def format_table_row(base, target, result, similarity_sum, similarity_avg):
    """Formata uma linha da tabela com os resultados."""
    result_str = str(result)
    result_str = result_str[:60]
    row = f"| {base:<14} | {target:<14} | {similarity_sum:>18.2f} | {similarity_avg:>18.2f} | {result_str:<48} |"
    return row

def evaluate_analogies(model, analogies, topn=TOPN):
    """Avalia a acurácia do modelo Word2Vec usando um conjunto de analogias e salva os resultados em um arquivo."""
    total_accuracy = 0
    total_analogies = len(analogies)

    # Formatar e exibir o cabeçalho
    header, line = format_table_header()
    print(header)
    print(line)
    
    for base, target in analogies:
        if base in model.wv and target in model.wv:
            # Calcula as palavras mais similares à palavra base
            words = [word for word, _ in model.wv.most_similar(base, topn=topn)]

            similarity_sum = 0
            words_str = ""
            for word in words:
                similarity = 0
                similarity = model.wv.similarity(target, word)
                # words_str = words_str + word +" "+ str(similarity) + ", "
                words_str = words_str + word + ", "
                similarity_sum += similarity
            similarity_avg = similarity_sum / topn
            total_accuracy = total_accuracy + similarity_avg
            

            row = format_table_row(base, target, words_str, similarity_sum, similarity_avg)
            print(row)
            

    overall_accuracy = total_accuracy / total_analogies  
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
    print(f'\nAcurácia do modelo: {accuracy}')

if __name__ == "__main__":
    main()
