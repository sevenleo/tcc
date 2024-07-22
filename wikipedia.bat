@echo off
REM Ativa o ambiente virtual
call venv\Scripts\activate.bat

REM Muda o diretório para a pasta desejada
cd /d "word2vec/WIKIPEDIA"

REM Mantém o terminal aberto
cmd /k
