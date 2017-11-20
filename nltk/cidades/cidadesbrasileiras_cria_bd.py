# coding=latin1

#http://pythonclub.com.br/gerenciando-banco-dados-sqlite3-python-parte1.html
#CREATE TABLE IF NOT EXISTS 'pais' (
#  'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#  'nome' VARCHAR(60) DEFAULT NULL,
#  'sigla' VARCHAR(10) DEFAULT NULL
#) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

#INSERT INTO 'pais' ('id', 'nome', 'sigla') VALUES (1, 'Brasil', 'BR');

#CREATE TABLE IF NOT EXISTS 'estado' (
#  'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#  'nome' VARCHAR(75) DEFAULT NULL,
#  'uf' VARCHAR(5) DEFAULT NULL,
#  'pais' INTEGER DEFAULT NULL,
#  KEY 'fk_Estado_pais' ('pais')
#) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=28 ;

#CREATE TABLE IF NOT EXISTS 'cidade' (
#  'id' INTEGER NOT NULL AUTO_INCREMENT,
#  'nome' VARCHAR(120) DEFAULT NULL,
#  'estado' INTEGER DEFAULT NULL,
#  PRIMARY KEY ('id'),
#  KEY 'fk_Cidade_estado' ('estado')
#) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5565 ;


import sqlite3
DEBUG = False


def executeScriptsFromFile(comandsfilename,dbcursor):
	# Open and read the file as a single buffer
	print("Lendo arquivos de comandos\n")
	fd = open(comandsfilename, 'r')
	sqlFile = fd.read()
	fd.close()

	# all SQL commands (split on ';')
	print("carregando comandos\n")
	sqlCommands = sqlFile.split(';')


	#TEST
	if DEBUG:
		try:
			cursor.execute("CREATE TABLE clientes (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,					 nome TEXT NOT NULL,					 idade INTEGER,					 cpf	  VARCHAR(11) NOT NULL,					 email TEXT NOT NULL,					 fone TEXT,					 cidade TEXT,					 uf VARCHAR(2) NOT NULL,					 criado_em DATE NOT NULL		  ); ")
			print ("** done\n")
		except Exception as e:
			if "UNIQUE constraint failed" in str(e):
				print(command[:50]+"...")
				print("*** tabela ja existe\n")
			else:
				print ("***** skipped: "+ str(e)+"\n")
	else:
		# Execute every command from the input file
		print("realizando comandos\n")
		error=0
		done=0
		for command in sqlCommands:
			# This will skip and report errors
			# For example, if the tables do not yet exist, this will skip over
			# the DROP TABLE commands
			try:
				dbcursor.execute(command)
				done=done+1
				#print ("** done\n")
			except Exception as e:
				if "UNIQUE constraint failed" in str(e):
					print(command[:50]+"...")
					print("*** tabela ja existe\n")
				else:
					print ("***** skipped: "+ str(e)+"\n")
					error=error+1

		print("fim das tarefas\n")
		print("sucessos : "+str(done))
		print("falhas : "+str(error))


print("iniciando\n")
# connect_db.py
print("conectando bd\n")
conn = sqlite3.connect('cidadesbrasileiras.db')
cursor = conn.cursor()
executeScriptsFromFile('cidadesbrasileiras.sql',cursor)
print("finalizando\n")
# gravando no bd
conn.commit()
print('Dados gravados com sucesso.\n')




tabela='pais'
tabela='cidade'
tabela='estado'

print("Print da tabela:\n\t"+tabela)
cursor.execute("SELECT * FROM "+tabela);
try:
	for linha in cursor.fetchall():
		print(linha)
except:
	#caso a tabela tenha somente uma linha
	pass



# Para visualizar/ler no windows com o software
# sqlitestudio
# ou
# SQLiteDatabaseBrowser