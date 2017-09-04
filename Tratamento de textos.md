# **Tratando um texto:**

Repassando para saber se entendi bem o passo a passo e não inverti a ordem das coisas.

-   Quebrar em tokens (um bom parser ja faz isso)

-   Criar um dicionario para aquele contexto ou continuar utilizando um já existente (com python ex.:[link](http://orion.lcg.ufrj.br/python/_06%20-%20Programando%20em%20Python%20-%20Dicionarios.pdf))

-   classificar os tokens gramaticalmente (parser)

-   classificar os tokens contextualmente

-   **...**



------------------------------------------------------------------------------------

# **Definições**

A tokenizer breaks a stream of text into tokens, usually by looking for whitespace (tabs, spaces, new lines).

A lexer is basically a tokenizer, but it usually attaches extra context to the tokens -- this token is a number, that token is a string literal, this other token is an equality operator.

A parser takes the stream of tokens from the lexer and turns it into an abstract syntax tree representing the (usually) program represented by the original text.



------------------------------------------------------------------------------------
# **I - PARSERs**


## **1) NLTK**

http://docs.huihoo.com/nltk/0.9.5/guides/portuguese_en.html

http://www.nltk.org/howto/portuguese_en.html

Feedback:

import nltk; nltk.download(); 
O dowloader não está baixando arquivos de todos os módulos necessários, tentei baixar alguns manualmente mas nem todos estão online.

Encontrei 3 pacotes em portugues:
mac_morpho (sao carlos)
machado (obras de machado de assis)
floresta (...)

Tive que baixar atraves dos links que estavam no xml :
https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/index.xml
e colocar na pasta
C:\Users\Leo\AppData\Roaming\nltk_data\

Empaquei neste erro:
Resource 'tokenizers/punkt/english.pickle' not found.  Please use the NLTK Downloader to obtain the resource

Há o arquivo english.pickle na pasta e até mesmo o portugues.pickle
![Erro1](https://github.com/sevenleo/tcc/blob/master/nltk_error.jpg)
![Erro2](https://github.com/sevenleo/tcc/blob/master/nltk_error2.jpg)

------------------------------------------------------------------------------------


## **2) Syntaxnet**

Um parser do Google/Tensorflow que usa NLTK e python

http://davidsbatista.net/blog/2017/03/25/syntaxnet/


HTTP API for Portuguese

http://davidsbatista.net/blog/2017/07/22/SyntaxNet-API-Portuguese/


Demostração (web app):

http://syntaxnet.askplatyp.us/v1#!/default/post_parsey_universal_full


Github com passos da instalação (serve para ingles e portugues)

https://github.com/davidsbatista/syntaxnet-api


Github com uso somente em portugues

https://github.com/davidsbatista/syntaxnet-api


Método mais "fácil de instalação" é usando o docker:

https://www.docker.com/docker-windows


Imagens em docker

https://hub.docker.com/r/tensorflow/syntaxnet/


Feedback:
Demorou horas a instalação do docker e da sua imagem. Veio cheio de erros e não funcionou.

![Erro1](https://github.com/sevenleo/tcc/blob/master/Syntaxnet-error.jpg)


------------------------------------------------------------------------------------



## **3) NLPNET**
natural Language Processing with neural networks
ainda não testei este
https://pypi.python.org/pypi/nlpnet/

------------------------------------------------------------------------------------



# **II - Criando dicionários com o python:**

-   http://defpython.blogspot.com.br/2007/01/conhecendo-os-dicionrios.html

-   http://orion.lcg.ufrj.br/python/_06%20-%20Programando%20em%20Python%20-%20Dicionarios.pdf



------------------------------------------------------------------------------------
# **Outros links importantes:**
https://pt.slideshare.net/pugpe/nlt
http://www.fgv.br/emap/logonto-2011/slides/leonel.pdf
https://github.com/fmaruki/Nltk-Tagger-Portuguese
https://pypi.python.org/pypi/nlpnet/

------------------------------------------------------------------------------------
### *Formatação do texto*
-	Instruções
	-	https://pt.wikipedia.org/wiki/Markdown
	-	https://guides.github.com/features/mastering-markdown/
-	Richtext 2 markdown(md)
	-	http://euangoddard.github.io/clipboard2markdown/
	-	http://markitdown.medusis.com/