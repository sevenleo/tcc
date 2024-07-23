import os
import logging
from gensim.models import Word2Vec
from tabulate import tabulate

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminhos para os modelos Word2Vec
clueweb_model_path = 'clueweb/modelo/word2vec.model'
wikipedia_model_path = 'wikipedia/modelo/word2vec.model'

# Função para carregar o modelo
def load_model(model_path):
    if os.path.exists(model_path):
        logger.info(f'Carregando o modelo Word2Vec de {model_path}')
        model = Word2Vec.load(model_path)
        return model
    else:
        logger.error(f'Modelo não encontrado em {model_path}')
        return None

# Função para calcular similaridade entre duas palavras
def calcular_similaridade(palavra1, palavra2, model):
    if palavra1 in model.wv.key_to_index and palavra2 in model.wv.key_to_index:
        similaridade = model.wv.similarity(palavra1, palavra2)
        return similaridade
    else:
        logger.error('Uma ou ambas as palavras não estão no vocabulário do modelo.')
        return None

if __name__ == "__main__":
    while True:
        # Solicitar o tipo de pesquisa ao usuário
        escolha = input("Digite 'CLUEWEB' para o modelo CLUEWEB, 'WIKIPEDIA' para o modelo WIKIPEDIA, 'COMPARAR' para comparar ambos ou 'SAIR' para finalizar: ").strip().upper()
        
        if escolha == 'SAIR':
            break
        
        if escolha == 'CLUEWEB':
            model = load_model(clueweb_model_path)
        elif escolha == 'WIKIPEDIA':
            model = load_model(wikipedia_model_path)
        elif escolha == 'COMPARAR':
            model_clueweb = load_model(clueweb_model_path)
            model_wikipedia = load_model(wikipedia_model_path)
        else:
            print("Opção inválida. Por favor, escolha 'CLUEWEB', 'WIKIPEDIA', 'COMPARAR' ou 'SAIR'.")
            continue

        if escolha in ['CLUEWEB', 'WIKIPEDIA'] and model is None:
            continue
        if escolha == 'COMPARAR' and (model_clueweb is None or model_wikipedia is None):
            continue

        while True:
            # Solicitar as duas palavras ao usuário
            entrada = input("Digite duas palavras separadas por espaço (ou 'voltar' para escolher outro modelo): ").strip()
            
            if entrada.lower() == 'voltar':
                break
            
            palavras = entrada.split()
            if len(palavras) != 2:
                print("Por favor, digite exatamente duas palavras separadas por espaço.")
                continue
            
            palavra1, palavra2 = palavras
            
            if escolha == 'COMPARAR':
                # Calcular a similaridade em ambos os modelos
                similaridade_clueweb = calcular_similaridade(palavra1, palavra2, model_clueweb)
                similaridade_wikipedia = calcular_similaridade(palavra1, palavra2, model_wikipedia)
                
                if similaridade_clueweb is not None and similaridade_wikipedia is not None:
                    tabela = [
                        ["Modelo", "Similaridade"],
                        ["CLUEWEB", similaridade_clueweb],
                        ["WIKIPEDIA", similaridade_wikipedia]
                    ]
                    print(tabulate(tabela, headers="firstrow", tablefmt="grid"))
                else:
                    print("Não foi possível calcular a similaridade em um ou ambos os modelos. Verifique se as palavras estão no vocabulário dos modelos.")
            else:
                # Calcular a similaridade no modelo selecionado
                similaridade = calcular_similaridade(palavra1, palavra2, model)
                
                if similaridade is not None:
                    print(f"A similaridade entre '{palavra1}' e '{palavra2}' no modelo {escolha} é: {similaridade}")
                else:
                    print("Não foi possível calcular a similaridade. Verifique se as palavras estão no vocabulário do modelo.")
