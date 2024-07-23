import gensim
import os

def generate_latex_table(word, topn, model, model_name, output_file):
    print('\n')

    # Obter as N palavras mais similares
    try:
        similar_words = model.wv.most_similar(word, topn=topn)
    except:
        print('Palavra nao encontrada no Vocabulario')
        return False

    # Criar e abrir o arquivo de saída
    with open(output_file, 'a') as f:
        f.write(r'\begin{table}[H]' + '\n')
        f.write(r'\centering' + '\n')
        f.write(r'\begin{tabular}{|c | c|}' + '\n')
        f.write(r' \hline' + '\n')
        f.write(f' Palavra similares a ({word}) & Similaridade \\\\ [0.5ex]' + '\n')
        f.write(r' \hline' + '\n')

        # Mostrar e escrever os resultados
        print('(Modelo:'+model_name+')\tPalavras similares a '+word+':')
        for word_sim, similarity in similar_words:
            # Exibir resultados no terminal
            print(f'{word_sim: <25} {similarity:.8f}')
            
            # Escrever resultados no arquivo LaTeX
            f.write(f' {word_sim} & {similarity:.8f} \\\\' + '\n')
            f.write(r' \hline' + '\n')

        f.write(r'\end{tabular}' + '\n')
        f.write(f'\\caption{{Resultados de palavras similares a palavra \'{word}\' segundo o modelo \'{model_name}\'.}}' + '\n')
        f.write(r'\label{table:1}' + '\n')
        f.write(r'\end{table}' + '\n')
        f.write(r'\n\n\n')
        print('\n')
        print(f"Tabela gerada e salva em {output_file}")
        return True

if __name__ == "__main__":
    '''
    # Seleção do modelo
    print("Escolha o modelo:")
    print("1. ClueWeb")
    print("2. Wikipedia")
    choice = input("Digite o número correspondente ao modelo desejado: ")

    if choice == '1':
        model_path = 'clueweb/modelo/word2vec.model'
        model_name = 'Clueweb'
    elif choice == '2':
        model_path = 'wikipedia/modelo/word2vec.model'
        model_name = 'Wikipedia'
    else:
        print("Escolha inválida. Saindo...")
        exit(1)
    
    '''

    # Número de palavras similares a serem retornadas
    topn = int(input("Digite o número de palavras similares a serem retornadas: "))
    
  

    while True:
        # Palavra para análise
        word = input("Digite a palavra para análise: ")

        model_name1 = 'Clueweb'
        model_path1 = model_name1.lower()+'/modelo/word2vec.model'
        output_file1 = 'predicts.'+model_name1+'.tex'
        model1 = gensim.models.Word2Vec.load(model_path1)
        
        model_name2 = 'Wikipedia'
        model_path2 = model_name2.lower()+'/modelo/word2vec.model'
        output_file2 = 'predicts.'+model_name2+'.tex'
        model2 = gensim.models.Word2Vec.load(model_path2)


        generate_latex_table(word, topn, model1, model_name1, output_file1)
        generate_latex_table(word, topn, model2, model_name2, output_file2)
        
