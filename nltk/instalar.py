import os
os.system("sudo apt-get install python-pip")  
os.system("sudo pip install --upgrade pip")  
os.system("sudo pip install setuptools")  
os.system("sudo pip install nltk")  
os.system("sudo pip install unidecode")  
os.system("sudo pip install BeautifulSoup4")
os.system("sudo pip install beautifulsoup")

import nltk
nltk.download('mac_morpho')
nltk.download('floresta')
nltk.download('machado')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
