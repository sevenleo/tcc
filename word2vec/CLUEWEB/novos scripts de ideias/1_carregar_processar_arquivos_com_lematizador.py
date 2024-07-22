import os
import re
import gzip
import logging
import numpy as np
import gensim
from gensim.models import Word2Vec
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer
import nltk
import datetime
import unidecode

# Certifique-se de baixar os stopwords e o tokenizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('rslp')  # Baixar o lematizador para português

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho para os dados do ClueWeb09
data_path = '../../clueweb09-pt'
results_folder = 'modelo/'

# Garantir que a pasta de resultados exista
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

progress_log = os.path.join(results_folder, 'progress_log.txt')
model_path = os.path.join(results_folder, 'word2vec.model')
matrix_path = os.path.join(results_folder, 'word_matrix.npy')
vocab_path = os.path.join(results_folder, 'vocabulary.txt')
info_path = os.path.join(results_folder, 'info.txt')

# Variáveis para rastreamento
total_words_processed = 0
total_files_processed = 0

# Função para carregar e limpar os dados
def load_and_preprocess_data(file_path):
    stop_words = set(stopwords.words('portuguese'))
    stemmer = RSLPStemmer()
    documents = []
    logger.info(f'Lendo o arquivo {file_path}')
    
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        text = f.read()
        #text = unidecode.unidecode(text)  # Remover acentos
        #text = re.sub(r'\d+', '', text)  # Remove números
        #text = re.sub(r'[^\w\s]', '', text)  # Remove pontuação
        #text = re.sub(r'\s+', ' ', text)  # Remove espaços extras
        words = word_tokenize(text)
        
        # Inicializa uma lista vazia para armazenar as palavras processadas
        processed_words = []

        # Itera sobre cada palavra na lista de palavras
        for word in words:
            word_start = word

            #palavras em minusculo
            word = word.lower()

            # Verifica se a palavra contém apenas letras e não é uma stop word
            if word.isalpha() and word not in stop_words:
                #word = unidecode.unidecode(word)  # Remover acentos
                word = re.sub(r'\d+', '', word)  # Remove números
                word = re.sub(r'[^\w\s]', '', word)  # Remove pontuação
                word = re.sub(r'\s+', ' ', word)  # Remove espaços extras
                # Aplica o stemmer na palavra e adiciona à lista de palavras processadas
                processed_word = stemmer.stem(word)
                processed_words.append(processed_word)
                #print ("Limpeza da palavra : "+word_start+" > "+word)

        # Atualiza a lista de documentos com as palavras processadas
        documents.extend(processed_words)
    
    return documents


# Função para treinar ou continuar o modelo Word2Vec
def train_or_continue_model(documents, model):
    global total_words_processed
    if model is None:
        logger.info('Treinando um novo modelo Word2Vec')
        model = Word2Vec(sentences=[documents], vector_size=100, window=5, min_count=5, workers=4)
    else:
        logger.info('Atualizando o modelo Word2Vec existente')
        model.build_vocab([documents], update=True)
    
    try:
        model.train([documents], total_examples=model.corpus_count, epochs=model.epochs)
    except KeyboardInterrupt:
        logger.info('Processamento interrompido pelo usuário. Salvando o progresso...')
    
    total_words_processed += len(documents)
    model.save(model_path)
    save_word_matrix_and_vocab(model, matrix_path, vocab_path)
    logger.info('Modelo Word2Vec treinado e salvo')
    return model

# Função para carregar o modelo existente
def load_existing_model_and_matrix():
    model = None
    if os.path.exists(model_path):
        logger.info(f'Carregando o modelo Word2Vec existente de {model_path}')
        model = Word2Vec.load(model_path)
    
    return model

# Função para registrar o progresso
def log_progress(file_path):
    with open(progress_log, 'a') as log_file:
        log_file.write(f"{file_path}\n")

# Função para carregar o progresso registrado
def load_progress():
    if os.path.exists(progress_log):
        with open(progress_log, 'r') as log_file:
            return set(line.strip() for line in log_file)
    return set()

# Função para salvar a matriz de palavras e o vocabulário
def save_word_matrix_and_vocab(model, matrix_path, vocab_path):
    # Salvar a matriz de palavras
    word_matrix = model.wv.vectors
    np.save(matrix_path, word_matrix)
    
    # Salvar o vocabulário com encoding 'utf-8'
    with open(vocab_path, 'w', encoding='utf-8') as f:
        for word in model.wv.index_to_key:
            f.write(f"{word}\n")

    # Salvar informações técnicas
    with open(info_path, 'w', encoding='utf-8') as info_file:
        info_file.write(f"Data de execução: {datetime.datetime.now()}\n")
        info_file.write(f"Número total de palavras processadas: {total_words_processed}\n")
        info_file.write(f"Número total de arquivos processados: {total_files_processed}\n")
        
        if os.path.exists(model_path):
            model = Word2Vec.load(model_path)
            info_file.write(f"Número de palavras no modelo: {len(model.wv.index_to_key)}\n")
            info_file.write(f"Tamanho dos vetores de palavras: {model.vector_size}\n")
        
        if os.path.exists(matrix_path):
            matrix = np.load(matrix_path)
            info_file.write(f"Forma da matriz de palavras: {matrix.shape}\n")

# Função para processar arquivos e salvar o progresso
def process_files(data_path):
    global total_words_processed, total_files_processed
    model = load_existing_model_and_matrix()
    processed_files = load_progress()
    
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file.endswith('.gz'):
                file_path = os.path.join(root, file)
                
                # Verificar se o arquivo já foi processado
                if file_path not in processed_files:
                    documents = load_and_preprocess_data(file_path)
                    total_words_processed += len(documents)
                    model = train_or_continue_model(documents, model)
                    log_progress(file_path)
                    total_files_processed += 1

    # Atualiza as informações técnicas após o processamento de todos os arquivos
    save_word_matrix_and_vocab(model, matrix_path, vocab_path)

if __name__ == "__main__":
    process_files(data_path)
