import numpy as np
from gensim.models import Word2Vec
import keyboard
import nltk
from datetime import datetime
import os

# Caminho padrão para salvar os resultados
default_save_path = os.getcwd()

# Caminho para o arquivo da matriz de palavras
matrix_path = 'modelo/word_matrix.npy'
# Caminho para o arquivo do vocabulário
vocab_path = 'modelo/vocabulary.txt'
# Caminho para o arquivo do modelo Word2Vec
model_path = 'modelo/word2vec.model'

def load_matrix_and_vocab(matrix_path, vocab_path):
    # Carregar a matriz de palavras
    word_matrix = np.load(matrix_path)
    
    # Carregar o vocabulário com encoding 'utf-8'
    with open(vocab_path, 'r', encoding='utf-8') as f:
        vocabulary = [line.strip() for line in f]
    
    return word_matrix, vocabulary

def load_model(model_path):
    # Carregar o modelo Word2Vec
    return Word2Vec.load(model_path)

def get_word_vector(word, word_matrix, vocabulary):
    if word in vocabulary:
        index = vocabulary.index(word)
        return word_matrix[index]
    else:
        return None

def print_similar_words(model, word, topn=10):
    result = f"\n10 palavras mais similares a '{word}':\n"
    try:
        similar_words = model.wv.most_similar(word, topn=topn)
        max_word_length = max(len(similar_word) for similar_word, _ in similar_words)
        max_similarity_length = max(len(f"{similarity:.4f}") for _, similarity in similar_words)
        
        border = "+" + "-" * (max_word_length + 2) + "+" + "-" * (max_similarity_length + 2) + "+"
        result += border + "\n"
        result += f"| {'Palavra'.ljust(max_word_length)} | {'Similaridade'.rjust(max_similarity_length)} |\n"
        result += border + "\n"
        
        for similar_word, similarity in similar_words:
            result += f"| {similar_word.ljust(max_word_length)} | {similarity:.4f}".rjust(max_similarity_length + 1) + " |\n"
        result += border + "\n"
    except KeyError:
        result += f"A palavra '{word}' não está no vocabulário.\n"
    return result


def save_results(word, results, save_path):
    # Criar a pasta com o nome "resultados de [data de hoje]" se não existir
    today_date = datetime.now().strftime("%Y-%m-%d")
    folder_name = f"resultados de {today_date}"
    folder_path = os.path.join(save_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    # Salvar os resultados em um arquivo .txt com o nome da palavra
    file_path = os.path.join(folder_path, f"{word}.txt")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(results)

if __name__ == "__main__":
    # Carregar a matriz de palavras, vocabulário e modelo
    word_matrix, vocabulary = load_matrix_and_vocab(matrix_path, vocab_path)
    model = load_model(model_path)
    
    while True:
        word = input("Digite a palavra para consultar (ou 'sair' para encerrar): ").strip().lower()
        if word == 'sair':
            break
        
        # Consultar o vetor da palavra
        vector = get_word_vector(word, word_matrix, vocabulary)
        results = f"\nVetor da palavra '{word}':\n{vector}\n" if vector is not None else f"A palavra '{word}' não está no vocabulário.\n"
        
        # Mostrar palavras similares e predições
        results += print_similar_words(model, word)
        
        # Exibir no terminal
        print(results)
        
        # Salvar os resultados em um arquivo
        save_results(word, results, default_save_path)
