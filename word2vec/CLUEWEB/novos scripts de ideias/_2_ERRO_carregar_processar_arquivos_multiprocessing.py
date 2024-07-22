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
import time
import signal
from multiprocessing import Pool

# Certifique-se de baixar os stopwords e o tokenizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('rslp')  # Baixar o lematizador para português

# Configuração do logging
logging.basicConfig(level=logging.INFO, handlers=[
    logging.FileHandler("modelo/terminal.txt"),
    logging.StreamHandler()
])
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

# Limite de arquivos processados simultaneamente
max_processes = 1

# Variável para controlar o estado de interrupção
interrupted = False

# Manipulador de sinal para interrupções
def signal_handler(sig, frame):
    global interrupted
    logger.info('Interrupção detectada. Encerrando o processo...')
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)

# Função para carregar e limpar os dados
def load_and_preprocess_data(file_path):
    stop_words = set(stopwords.words('portuguese'))
    stemmer = RSLPStemmer()
    documents = []
    logger.info(f'Lendo o arquivo {file_path}')
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        text = f.read().lower()
        text = unidecode.unidecode(text)  # Remover acentos
        text = re.sub(r'\d+', '', text)  # Remove números
        text = re.sub(r'[^\w\s]', '', text)  # Remove pontuação
        text = re.sub(r'\s+', ' ', text)  # Remove espaços extras
        words = word_tokenize(text)
        words = [stemmer.stem(word) for word in words if word.isalpha() and word not in stop_words]
        documents.extend(words)
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
        raise  # Relevante para o Pool de multiprocessing encerrar corretamente
    
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

# Função para registrar o progresso de forma segura
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

# Função para processar um arquivo e salvar o progresso
def process_file(file_path):
    global total_words_processed, total_files_processed
    start_time = time.time()
    
    if interrupted:
        logger.info('Processo interrompido. Abortando a execução.')
        return

    processed_files = load_progress()
    if file_path not in processed_files:
        documents = load_and_preprocess_data(file_path)
        model = train_or_continue_model(documents, load_existing_model_and_matrix())
        total_words_processed += len(documents)
        total_files_processed += 1
        log_progress(file_path)
    
    end_time = time.time()
    processing_time = end_time - start_time
    logger.info(f'Tempo para processar {file_path}: {processing_time:.2f} segundos')
    return file_path

def process_files_in_batches(files_to_process, max_processes):
    global interrupted
    for i in range(0, len(files_to_process), max_processes):
        batch = files_to_process[i:i+max_processes]
        with Pool(processes=max_processes) as pool:
            results = pool.map(process_file, batch)
            if interrupted:
                logger.info('Processo interrompido. Abortando as tarefas restantes.')
                pool.terminate()
                break

def process_files(data_path, max_processes):
    # Obter lista de arquivos a serem processados
    files_to_process = []
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file.endswith('.gz'):
                file_path = os.path.join(root, file)
                files_to_process.append(file_path)

    # Carregar e processar arquivos em lotes
    process_files_in_batches(files_to_process, max_processes)

    # Atualiza as informações técnicas após o processamento de todos os arquivos
    save_word_matrix_and_vocab(load_existing_model_and_matrix(), matrix_path, vocab_path)

if __name__ == "__main__":
    process_files(data_path, max_processes)
