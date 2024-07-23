import os
from gensim.models import Word2Vec

# Função para calcular a similaridade entre duas palavras
def calcular_similaridade(modelo, palavra1, palavra2):
    try:
        similaridade = modelo.wv.similarity(palavra1, palavra2)
    except KeyError as e:
        print(f"Palavra não encontrada no modelo: {e}")
        similaridade = None
    return similaridade

# Função para gerar a tabela de comparação em formato LaTeX
def gerar_tabela_latex(palavra1, palavra2, similaridade_clueweb, similaridade_wikipedia):
    tabela_latex = f"""
    \\begin{{table}}[h!]
    \\centering
    \\begin{{tabular}}{{|c |c | c|}} 
     \\hline
     Palavras & Modelo & Similaridade \\\\
     \\hline
     {palavra1} - {palavra2} & CLUEWEB & {similaridade_clueweb:.6f} \\\\
     {palavra1} - {palavra2} & WIKIPEDIA & {similaridade_wikipedia:.6f} \\\\
     \\hline
    \\end{{tabular}}
    \\caption{{Similaridade de cosseno entre as palavras {palavra1} \\& {palavra2}.}}
    \\label{{table:1}}
    \\end{{table}}
    """
    return tabela_latex

# Função para salvar a tabela de comparação em formato texto e LaTeX
def salvar_comparacao(palavra1, palavra2, similaridade_clueweb, similaridade_wikipedia):
    comparacoes_txt = "comparacoes.txt"
    comparacoes_latex = "comparacoes.latex"

    with open(comparacoes_txt, 'a', encoding='utf-8') as f_txt:
        f_txt.write(f"{palavra1} - {palavra2} | CLUEWEB | {similaridade_clueweb:.6f}\n")
        f_txt.write(f"{palavra1} - {palavra2} | WIKIPEDIA | {similaridade_wikipedia:.6f}\n")
    
    tabela_latex = gerar_tabela_latex(palavra1, palavra2, similaridade_clueweb, similaridade_wikipedia)
    
    with open(comparacoes_latex, 'a', encoding='utf-8') as f_latex:
        f_latex.write(tabela_latex)

# Função principal para comparar palavras entre os modelos
def comparar_modelos():
    # Carregar os modelos
    modelo_clueweb = Word2Vec.load("clueweb/modelo/word2vec.model")
    modelo_wikipedia = Word2Vec.load("wikipedia/modelo/word2vec.model")

    while True:
        entrada = input("Digite duas palavras separadas por espaço (ou 'sair' para encerrar): ")
        if entrada.lower() == 'sair':
            break
        
        palavras = entrada.split()
        if len(palavras) != 2:
            print("Por favor, digite exatamente duas palavras.")
            continue
        
        palavra1, palavra2 = palavras
        similaridade_clueweb = calcular_similaridade(modelo_clueweb, palavra1, palavra2)
        similaridade_wikipedia = calcular_similaridade(modelo_wikipedia, palavra1, palavra2)
        
        if similaridade_clueweb is not None and similaridade_wikipedia is not None:
            print(f"Similaridade no modelo CLUEWEB: {similaridade_clueweb:.6f}")
            print(f"Similaridade no modelo WIKIPEDIA: {similaridade_wikipedia:.6f}")
            
            salvar_comparacao(palavra1, palavra2, similaridade_clueweb, similaridade_wikipedia)
        else:
            print("Erro ao calcular similaridade. Verifique se as palavras existem nos modelos.")

if __name__ == "__main__":
    comparar_modelos()
