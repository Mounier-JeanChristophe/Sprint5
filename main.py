from os import path
import os
from glob import glob
import sys


#recherche les fichiers dans le dossier passé en parametre (chemin_dossier)
#qui finissent par l'extension passé en parametre.

def find_ext(chemin_dossier, ext):
    return glob(path.join(chemin_dossier, "*.{}".format(ext)))



def pdf_to_txt(inpute_path, output_path) :
    cmd = "pdftotext -raw " + inpute_path + " -bbox " + output_path
    os.system(cmd)


def find_paragraph(file_path, titre):
    paragraph = ""
    maChaine2 = "Abstract"
    pass1 = ""
    stop1 = "1"
    stop2 = "Key" 
    verif = True
    
    memorise = ""
    with open(file_path, "r") as file :
        for line in file :
        	if(verif == False):
        		break
        		
        	elif(line.find(maChaine2) != -1 or line.find("ABSTRACT") != -1):
        		while line:
        			line = file.readline()
        			position = line.find("<word")
        			str = line[position+76 : ]
        			position2 = str.find("</word>")
        			pass1 = str[0 : position2]
        			#print(pass1)
        			
        			if(pass1.find("Keywords:") != -1):
        				verif = False			
        				break
        			
        			if(pass1.find(stop1) != -1):
        				memorise = line
        				line = file.readline()
        				position = line.find("<word")
        				str = line[position+76 : ]
        				position2 = str.find("</word>")
        				pass1 = str[0 : position2]
        				if(pass1.find("Introduction") != -1 or pass1.find("INTRODUCTION") != -1 ):
        					verif = False			
        					break
        				else:
        					position = memorise.find(">")
        					str = memorise[position+1 : ]
        					position2 = str.find("</word>")
        					pass1 = str[0 : position2]
        					position = line.find(">")
        					str = line[position+1 : ]
        					position2 = str.find("</word>")
        					pass2 = str[0 : position2]
        					
        					paragraph = paragraph + pass1 + " " + pass2 + " "
             		
        			elif(pass1.find(stop2) != -1):
        				memorise = line
        				line = file.readline()
        				position = line.find("<word")
        				str = line[position+76 : ]
        				position2 = str.find("</word>")
        				pass1 = str[0 : position2]
        				if(pass1.find("words") != -1):
        					verif = False			
        					break
        				position = memorise.find(">")
        				str = memorise[position+1 : ]
        				position2 = str.find("</word>")
        				pass1 = str[0 : position2]
        				position = line.find(">")
        				str = line[position+1 : ]
        				position2 = str.find("</word>");
        				pass2 = str[0 : position2]
        				paragraph = paragraph + pass1 + " " + pass2 + " "
        			
        			
        			
        			else:
        				position = line.find(">")
        				str = line[position+1 : ]
        				position2 = str.find("</word>")
        				pass1 = str[0 : position2]
        				#print(pass1)
        				paragraph = paragraph + pass1 + " " 
             	
       	return paragraph
    return "Not Found\n"

#cree un dossier passe en parametre "dossier" dans le chemin passé en parametre "chemin"
def create_directory(dossier, chemin):
    directory_name = dossier
    path = chemin + "/" + directory_name
    if(os.path.isdir(path)):
        os.system("rm -r " + path)                  #supprimer le dossier s'il exit    
    os.system("mkdir " + path)                      #re creer le dossier
    return path    





def parser_file_to_txt(filepath, output_path) :

    file_name = os.path.basename(filepath).replace(".html", ".pdf")
    title = ""
    abstract = ""
    maChaine1 = "<title>"
    verif = True
    str2 = ""
    memorise = ""
    #   -- nom de fichier --

    f = open(output_path, "a")
    f.write("le nom de ce fichier est : " + file_name + "\n")
    f.close()

    f = open(filepath, "r")
    #for i in range(2) :
     #   title = title + f.readline().strip('\n').strip() + " "
    
    for ligne in f:
    	if(ligne.find(maChaine1) != -1):
    		position = ligne.find(maChaine1)
    		str = ligne[position+7 : ]
    		position2 = str.find("</title>");
    		title = str[0 : position2]
    		break
    f.close()
    
    			
    #   -- le titre de fichier --

    f = open(output_path, "a")
    f.write("\n\n le titre de ce fichier est  : " + title.rstrip() + "\n")
    f.close()
    
    #   -- abstract --

    abstract = find_paragraph(filepath, "abstract")
    f = open(output_path, "a")
    f.write("\n\n abstract : " + abstract)
    f.close()


def main():
    args = sys.argv
    filepath = args[1]   # on prends l'argument apres la commande python3 (chemin de dossier) si le code est dans le meme dossier des fichier il suffit just de mettre le nom de dossier                
    dossier_txt = create_directory("File_txt", filepath)
    dossier_output = create_directory("output", filepath)
    files = find_ext(filepath,"pdf")

    for file in files :
            #File_txt_path = dossier_txt + "/" + os.path.basename(file).replace(".pdf", ".txt")
            #output_path = dossier_output + "/" + os.path.basename(file).replace(".pdf", ".txt") 
            #pdf_to_txt(file, File_txt_path)
            #parser_file_to_txt(File_txt_path, output_path)

            File_txt_path = dossier_txt  + "/" + os.path.basename(file).replace(".pdf", ".html")
            output_path =  dossier_output + "/" + os.path.basename(file).replace(".pdf", ".txt")
            pdf_to_txt(file, File_txt_path)
            parser_file_to_txt(File_txt_path, output_path)
            
            
         
        

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
