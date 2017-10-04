import urllib2
from bs4 import BeautifulSoup

#qual pagina
link = 'http://www.globo.com'

#GET
page = urllib2.urlopen(link)

# parser, salva o body/html na variavel
soup = BeautifulSoup(page, 'html.parser')


#busca a primeira ocorrencia com find ou busca todas com findAll
noticias = soup.findAll('a', attrs={'class': 'hui-premium__link'})
for n in noticias:
	print("Noticia ["+str(noticias.index(n)+1)+"] "+n.text.strip())

