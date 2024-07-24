import gensim
import numpy as np
import os
from datetime import datetime

# Número de predições consideradas para cada analogia
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
            if len(parts) == 4:
                analogies.append(parts)
    return analogies

def evaluate_analogies(model, analogies, topn=TOPN):
    """Avalia a acurácia do modelo Word2Vec usando um conjunto de analogias e salva os resultados em um arquivo."""
    total_accuracy = 0
    total_analogies = len(analogies)
    results = []

    for a, b, c, d in analogies:
        if a in model.wv and b in model.wv and c in model.wv:
            # Calcula a analogia
            result = model.wv.most_similar(positive=[b, c], negative=[a], topn=topn)
            
            # Adiciona os resultados das top N palavras mais similares
            similar_words = [word for word, _ in result]
            accuracy_analogy = 1 if d in similar_words else 0
            total_accuracy += accuracy_analogy

            # Adiciona o resultado à lista
            results.append((a, b, c, d, similar_words, accuracy_analogy))

    overall_accuracy = total_accuracy / total_analogies if total_analogies > 0 else 0

    # Prepara o conteúdo para salvar em arquivo
    output_lines = []
    output_lines.append("Resultado das Analogias")
    output_lines.append(f"{'A':<10} | {'B':<10} | {'C':<10} | {'D':<15}  | {'Acurácia da Analogias':<20} | {'Palavras Preditas':<40}")
    output_lines.append("-" * 110)
    for a, b, c, d, similar_words, accuracy_analogy in results:
        similar_words_str = ', '.join(similar_words)
        output_lines.append(f"{a:<10} | {b:<10} | {c:<10} | {d:<15} | {accuracy_analogy:.4f} | {similar_words_str:<40} ")

    output_lines.append(f'\nAcurácia do modelo: {overall_accuracy:.2%}')

    # Cria a pasta para os resultados com a data de hoje
    today_date = datetime.now().strftime("%Y-%m-%d")
    results_folder = f"resultados de {today_date}"
    os.makedirs(results_folder, exist_ok=True)

    # Define o caminho para o arquivo de resultados
    output_file = os.path.join(results_folder, 'acuracia.txt')

    # Salva o conteúdo em um arquivo
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(output_lines))

    # Exibe o conteúdo no terminal
    print('\n'.join(output_lines))

    return overall_accuracy

def main():
    model_path = 'modelo/word2vec.model'
    vocab_path = 'modelo/vocabulary.txt'
    analogy_file = 'analogias.txt'  # Substitua pelo caminho para seu arquivo de analogias

    # Verificar a existência dos arquivos antes de carregar
    if not (os.path.exists(model_path) and os.path.exists(vocab_path) and os.path.exists(analogy_file)):
        print("Erro: Certifique-se de que os arquivos de modelo, vocabulário e analogias existam.")
        return

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