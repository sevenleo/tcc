import gensim
import os

def generate_latex_table(word, topn, model_path, output_file):
    # Carregar o modelo Word2Vec
    model = gensim.models.Word2Vec.load(model_path)

    # Obter as N palavras mais similares
    similar_words = model.wv.most_similar(word, topn=topn)

    # Criar e abrir o arquivo de saída
    with open(output_file, 'w') as f:
        f.write(r'\begin{table}[h!]' + '\n')
        f.write(r'\centering' + '\n')
        f.write(r'\begin{tabular}{|c | c|}' + '\n')
        f.write(r' \hline' + '\n')
        f.write(r' Resultados & Similaridade (\%) \\ [0.5ex]' + '\n')
        f.write(r' \hline\hline' + '\n')

        for word, similarity in similar_words:
            f.write(f' {word} & {similarity:.8f} \\' + '\n')
            f.write(r' \hline' + '\n')

        f.write(r'\end{tabular}' + '\n')
        f.write(f'\caption{{Resultados de palavras preditas para a palavra \'{word}\'.}}' + '\n')
        f.write(r'\label{table:1}' + '\n')
        f.write(r'\end{table}' + '\n')

if __name__ == "__main__":
    # Seleção do modelo
    print("Escolha o modelo:")
    print("1. ClueWeb")
    print("2. Wikipedia")
    choice = input("Digite o número correspondente ao modelo desejado: ")

    if choice == '1':
        model_path = 'clueweb/modelo/word2vec.model'
    elif choice == '2':
        model_path = 'wikipedia/modelo/word2vec.model'
    else:
        print("Escolha inválida. Saindo...")
        exit(1)

    # Palavra para análise
    word = input("Digite a palavra para análise: ")
    
    # Número de palavras similares a serem retornadas
    topn = int(input("Digite o número de palavras similares a serem retornadas: "))
    
    # Arquivo de saída
    output_file = 'predicts.tex'

    generate_latex_table(word, topn, model_path, output_file)
    print(f"Tabela gerada e salva em {output_file}")
