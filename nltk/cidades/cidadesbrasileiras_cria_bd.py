import sqlite3
def executeScriptsFromFile(comandsfilename,dbcursor):
    # Open and read the file as a single buffer
    print("Lendo arquivos de comandos")
    fd = open(comandsfilename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    print("carregando comandos")
    sqlCommands = sqlFile.split(';')


    
    # Execute every command from the input file
    print("realizando comandos")
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        print("Command: "+command)
        try:
            dbcursor.execute(command)
            print ("\n* done")
        except Exception as e:
            print ("\n***** skipped: "+ str(e))

        print("fim das tarefas")

print("iniciando")
# connect_db.py
print("conectando bd")
conn = sqlite3.connect('cidadesbrasileiras.db')
cursor = conn.cursor()
executeScriptsFromFile('cidadesbrasileiras.sql',cursor)
#result = cursor.execute("SELECT * FROM table");
print("finalizando")