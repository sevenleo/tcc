import os
text = raw_input("Digite o nome do seu commit")
print ("..")
os.system("cd ..")
print ("add")
os.system("git add *")
print ("commit")
os.system("git commit -m"+text)
print ("push")
os.system("git push")
print ("ready")
os.system("cd nltk")