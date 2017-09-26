'''

INSTALAR
python 2.7
nltk
nltk: mac_morpho,floresta,machado


PASSO 1
baixar um texto
dar uma classificacao
tokenizar
fazer stemming nos tokens
classificar gramaticalmente os tokens_stemmizados (usando o mac_morpho de preferencia ou usando a api de um dicionario gratis qualquer)
salvar em um dicionario usando python

... 

PASSO 2
selecionar varios textos da web do mesmo assunto
e adicionar ao dicionario daquele assunto

...

PASSO N
pegar textos de blogs de acordo com as hashtags e adicionar aos dicionarios em que a hashtag se classificar

'''












import nltk

pensamento="Pensamento e pensar são, respectivamente, uma forma de processo mental ou faculdade do sistema mental.[1] Pensar permite aos seres modelarem sua percepção do mundo ao redor de si, e com isso lidar com ele de uma forma efetiva e de acordo com suas metas, planos e desejos. Palavras que se referem a conceitos e processos similares incluem cognição, senciência, consciência, ideia, e imaginação. O pensamento é considerado a expressão mais 'palpável' do espírito humano, pois através de imagens e ideias revela justamente a vontade deste. O pensamento é fundamental no processo de aprendizagem (vide Piaget). O pensamento é construto e construtivo do conhecimento. O principal veículo do processo de conscientização é o pensamento. A atividade de pensar confere ao homem 'asas' para mover-se no mundo e 'raízes' para aprofundar-se na realidade. Etimologicamente, pensar significa avaliar o peso de alguma coisa. Em sentido amplo, podemos dizer que o pensamento tem como missão tornar-se avaliador da realidade."
tokens(nltk.word_tokenizer(pensamento))
print (tokens)

