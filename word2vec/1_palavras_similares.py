import gensim
import os

def get_similar_words(word, topn, model):
    """Gera uma lista de palavras similares a partir de um modelo Word2Vec."""
    try:
        similar_words = model.wv.most_similar(word, topn=topn)
        return similar_words
    except KeyError:
        print('Palavra não encontrada no vocabulário')
        return None

def write_latex_table(word, similar_words, model_name, output_file):
    """Gera o código LaTeX e escreve no arquivo especificado."""
    file_exists = os.path.isfile(output_file)
    
    with open(output_file, 'a') as f:
    
        f.write(r'\begin{table}[H]' + '\n')
        f.write(r'\centering' + '\n')
        f.write(r'\begin{tabular}{|c | c|}' + '\n')
        f.write(r' \hline' + '\n')
        f.write(f' Palavra similares a ({word}) & Similaridade \\\\ [0.5ex]' + '\n')
        f.write(r' \hline' + '\n')

        for word_sim, similarity in similar_words:
            f.write(f' {word_sim} & {similarity:.8f} \\\\' + '\n')
            f.write(r' \hline' + '\n')

        f.write(r'\end{tabular}' + '\n')
        f.write(f'\\caption{{Palavras similares a palavra \'{word}\' segundo o modelo \'{model_name}\'.}}' + '\n')
        f.write(r'\label{table:1}' + '\n')
        f.write(r'\end{table}' + '\n')
        
        # Adicionar espaçamento vertical apropriado
        f.write('\n')  # Linha em branco

def print_similar_words(word, similar_words, model_name):
    """Imprime as palavras similares e suas similaridades no terminal."""
    print(f'(Modelo: {model_name})\tPalavras similares a {word}:')
    for word_sim, similarity in similar_words:
        print(f'{word_sim: <25} {similarity:.8f}')
    print('\n')

def txt_similar_words(word, similar_words, model_name):
    """Imprime as palavras similares e suas similaridades em um arquivo de texto."""
    # Define o nome do arquivo
    output_file = f'predicts.{model_name}.txt'
    
    # Abre o arquivo para escrita
    with open(output_file, 'a') as file:
        file.write(f'(Modelo: {model_name})\tPalavras similares a {word}:\n')
        for word_sim, similarity in similar_words:
            # Escreve os resultados no arquivo
            file.write(f'{word_sim: <25} {similarity:.8f}\n')
        file.write('\n')  # Linha em branco

if __name__ == "__main__":

    # Número de palavras similares a serem retornadas
    topn = int(input("Digite o número de palavras similares a serem retornadas: "))

    while True:
        # Palavra para análise
        word = input("Digite a palavra para análise: ")

        try:
            model_name1 = 'Clueweb'
            model_path1 = model_name1.lower() + '/modelo/word2vec.model'
            output_file1 = 'predicts.' + model_name1 + '.tex'
            model1 = gensim.models.Word2Vec.load(model_path1)
        except Exception as e:
            print(f"Erro ao carregar o modelo {model_name1}: {e}")
            continue
        
        try:
            model_name2 = 'Wikipedia'
            model_path2 = model_name2.lower() + '/modelo/word2vec.model'
            output_file2 = 'predicts.' + model_name2 + '.tex'
            model2 = gensim.models.Word2Vec.load(model_path2)
        except Exception as e:
            print(f"Erro ao carregar o modelo {model_name2}: {e}")
            continue

        # Obter palavras similares
        similar_words1 = get_similar_words(word, topn, model1)
        if similar_words1 is not None:
            # Imprimir no terminal e escrever no arquivo LaTeX para o modelo 1
            print_similar_words(word, similar_words1, model_name1)
            txt_similar_words(word, similar_words1, model_name1)
            write_latex_table(word, similar_words1, model_name1, output_file1)

        similar_words2 = get_similar_words(word, topn, model2)
        if similar_words2 is not None:
            # Imprimir no terminal e escrever no arquivo LaTeX para o modelo 2
            print_similar_words(word, similar_words2, model_name2)
            txt_similar_words(word, similar_words2, model_name2)
            write_latex_table(word, similar_words2, model_name2, output_file2)
