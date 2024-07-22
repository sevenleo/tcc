import os
import re
import logging
import numpy as np
from gensim.models import Word2Vec
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import datetime
from unicodedata import normalize
import multiprocessing

# Certifique-se de baixar os stopwords e o tokenizer
nltk.download('punkt')
nltk.download('stopwords')

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

data_path = '../../wikipedia-dumps'
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
    documents = []
    logger.info(f'Lendo o arquivo {file_path}')
    
    # Ler o arquivo em modo binário
    with open(file_path, 'rb') as f:
        raw_text = f.read()
    
    # Tentar decodificar o texto
    try:
        text = raw_text.decode('utf-8').lower()
    except UnicodeDecodeError:
        try:
            text = raw_text.decode('latin-1').lower()
        except UnicodeDecodeError as e:
            logger.error(f"Erro ao decodificar o arquivo {file_path}: {e}")
            return documents
    
    # Remover acentos
    text = normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    
    # Remove números e pontuação
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    
    # Tokeniza o texto
    words = word_tokenize(text)
    
    # Filtra palavras
    words = [word for word in words if word.isalpha() and word not in stop_words]

    # Remove stopwords
    words = [word for word in words if word not in stop_words]
    
    # Remove palavras menores que 3 caracteres
    words = [word for word in words if len(word) >= 3]

    # Estende a lista de documentos com as palavras limpas
    documents.extend(words)
    
    return documents

# Função para treinar ou continuar o modelo Word2Vec
def train_or_continue_model(documents, model):
    cpu_workers = multiprocessing.cpu_count()
    
    # Ajusta o número de workers para garantir desempenho
    if cpu_workers < 10:
        cpu_workers = max(1, cpu_workers - 2)
    else:
        cpu_workers = max(1, cpu_workers - 4)

    global total_words_processed
    if model is None:
        if len(documents) > 0:
            logger.info('Treinando um novo modelo Word2Vec')
            #model = Word2Vec(sentences=[documents], vector_size=100, window=10, min_count=5, workers=cpu_workers)
            model = Word2Vec(sentences=[documents], vector_size=300, window=30, min_count=10, workers=cpu_workers)
        else:
            logger.warning('Documento vazio. Ignorando.')
    else:
        if len(documents) > 0:
            logger.info('Atualizando o modelo Word2Vec existente')
            model.build_vocab([documents], update=True)
            model.train([documents], total_examples=model.corpus_count, epochs=model.epochs)
        else:
            logger.warning('Documento vazio. Ignorando.')
    
    if model:
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

# Função para salvar informações técnicas
def save_info():
    with open(info_path, 'a', encoding='utf-8') as info_file:
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
    global total_files_processed
    model = load_existing_model_and_matrix()
    processed_files = load_progress()
    
    # Apenas processa arquivos diretamente no diretório especificado
    files = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]
    
    for file in files:
        file_path = os.path.join(data_path, file)
        
        # Verificar se o arquivo já foi processado
        if file_path not in processed_files:
            documents = load_and_preprocess_data(file_path)
            model = train_or_continue_model(documents, model)
            log_progress(file_path)
            total_files_processed += 1
    
            save_info()

if __name__ == "__main__":
    process_files(data_path)
