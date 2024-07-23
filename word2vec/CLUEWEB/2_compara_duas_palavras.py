import os
import logging
from gensim.models import Word2Vec

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho para o modelo Word2Vec
model_path = 'modelo/word2vec.model'

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
    # Carregar o modelo
    model = load_model(model_path)
    
    if model:
        while True:
            # Solicitar as duas palavras ao usuário
            entrada = input("Digite duas palavras separadas por espaço (ou 'sair' para finalizar): ").strip()
            
            if entrada.lower() == 'sair':
                break
            
            palavras = entrada.split()
            if len(palavras) != 2:
                print("Por favor, digite exatamente duas palavras separadas por espaço.")
                continue
            
            palavra1, palavra2 = palavras
            
            # Calcular a similaridade
            similaridade = calcular_similaridade(palavra1, palavra2, model)
            
            if similaridade is not None:
                print(f"A similaridade entre '{palavra1}' e '{palavra2}' é: {similaridade}")
            else:
                print("Não foi possível calcular a similaridade. Verifique se as palavras estão no vocabulário do modelo.")
