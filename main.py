from os import path
import os
from glob import glob
import sys
from lxml import etree
import xml.etree.ElementTree as ET
import xml.dom.minidom as md


#recherche les fichiers dans le dossier passé en parametre (chemin_dossier)
#qui finissent par l'extension passé en parametre.

def find_ext(chemin_dossier, ext):
    return glob(path.join(chemin_dossier, "*.{}".format(ext)))



def pdf_to_txt(inpute_path) :
    cmd = "./pdfToText.sh "+inpute_path
    os.system(cmd)


def find_paragraph(file_path, titre):
    paragraph = ""
    linePrecedant = "aa"
    with open(file_path, "r") as file :
        for line in file :
            if(line.lower().find(titre) != -1): #or line.find(titre) != -1):   
                       	
                if(len(line) <= len(titre)+1):
                        line = file.readline()
                        while line == "\n":
                            line = file.readline()
                while line:
                    if(titre == "introduction") :
                        if((line[0:1] == "2" and linePrecedant.strip()[-1:] == ".") or (line[0:3] == "II." and linePrecedant.strip()[-1:] == ".")):
                             break   

                    else :
                        if(line.lower().strip() == "1 introduction" or line.strip() == "I. INTRODUCTION") :
                             break

                    paragraph = paragraph + line.strip() + " "
                    linePrecedant = line
                    line = file.readline()

                if(paragraph != "\n"):
                    return paragraph

            elif((titre == "Conclusion" and line.find(titre) != -1) or line.find("Conclusions") != -1 or titre.upper() in line):

                if(len(line) <= len(titre)+1):
                    line = file.readline()
                    while line == "\n":
                        line = file.readline()

                while line:
                    if(("References" in line or "REFERENCES" in line)):
                        break   

                    paragraph = paragraph + line.strip() + " "
                    linePrecedant = line
                    line = file.readline()

                if(paragraph != "\n"):
                    return paragraph

    return "Not Found\n"
def find_reference(file_path, titre):
    paragraph = ""
    with open(file_path, "r") as file :
        for line in file :
            if((line.find(titre) != -1 or line.find("REFERENCES") != -1) and len(line.strip())<=13):            	
                if(len(line) <= len(titre)+1):
                        line = file.readline()
                        while line == "\n":
                            line = file.readline()
                while line:
                    if(titre == "References" or titre.upper() == "REFERENCES") :
                        if(line is None) :
                             break
                    paragraph = paragraph + line.strip() + " "
                    line = file.readline()
                if(paragraph != "\n"):
                    return paragraph
    return "Not Found\n"
    
def find_discussion(file_path, titre):
    paragraph = ""
    with open(file_path, "r") as file :
        for line in file :
            if(line.find(titre) != -1 or line.find("DISCUSSION") != -1):            	
                if(len(line) <= len(titre)+1):
                        line = file.readline()
                        while line == "\n":
                            line = file.readline()
                while line:
                    if(titre == "Discussion" or titre.upper() == "DISCUSSION") :
                        if(((line.find("References") != -1 or line.find("REFERENCES") != -1 )and len(line.strip())<=11) or (line.find("Conclusions") != -1 or line.find("CONCLUSIONS") != -1 or line.find("Conclusion") != -1 or line.find("CONCLUSION") != -1)):
                             break
                    paragraph = paragraph + line.strip() + " "
                    line = file.readline()
                if(paragraph != "\n"):
                    return paragraph
    return "Not Found\n"


def find_corps(file_path):
    paragraph = ""
    linePrecedant = ""
    check = find_paragraph(file_path,"introduction")
    with open(file_path, "r") as file :
        for line in file :
            if(check == "Not Found\n"):
            	if(line[0:1] == "1" or line[0:3] == "I."):
                     while line:
                         if(line.find("Discussion") != -1 or line.find("DISCUSSION") != -1 or line.find("Conclusions") != -1 or line.find("CONCLUSIONS") != -1 or line.find("Conclusion") != -1 or line.find("CONCLUSION") != -1 or ((line.find("References") != -1 or line.find("REFERENCES") != -1) and len(line.strip())<=13)) :
                               break
                         paragraph = paragraph + line.strip() + " "
                         line = file.readline() 
                     return paragraph     
			    
            	linePrecedant = line
			    
            else:
            	if((line[0:1] == "2" and linePrecedant.strip()[-1:] == ".") or (line[0:3] == "II." and linePrecedant.strip()[-1:] == ".")):
                     while line:
                         if(line.find("Discussion") != -1 or line.find("DISCUSSION") != -1 or line.find("Conclusions") != -1 or line.find("CONCLUSIONS") != -1 or line.find("Conclusion") != -1 or line.find("CONCLUSION") != -1 or ((line.find("References") != -1 or line.find("REFERENCES") != -1) and len(line.strip())<=13)) :
                               break
                         paragraph = paragraph + line.strip() + " "
                         line = file.readline() 
                     return paragraph     
			    
            	linePrecedant = line
		    	
		    
            
    return "Not Found\n"

#cree un dossier passe en parametre "dossier" dans le chemin passé en parametre "chemin"
def create_directory(dossier):
    directory_name = dossier
    path = directory_name
    if(os.path.isdir(path)):
        os.system("rm -r " + path)                  #supprimer le dossier s'il exit    
    os.system("mkdir " + path)                      #re creer le dossier
    return path    



def parser_file_to_xml(target_path, output_path) :

    article = etree.Element("article")
    file_name = os.path.basename(target_path).replace(".txt", ".pdf")
    title = ""
    writer =""
    abstract = ""

    preamble = etree.SubElement(article, "preamble")
    preamble.text = file_name

    file = open(target_path, "r")
    for i in range(2) :
        title = title + file.readline().strip('\n').strip() + " "
    
    for line in file :
       if(line.lower().find("abstract") != -1):         
          break;
       writer = writer + line.strip('\n').strip()
        	
    file.close()
    
    
    
    

    titre = etree.SubElement(article, "titre")
    titre.text = title
    
    auteur = etree.SubElement(article, "auteur")
    auteur.text = writer
    
    abstract = etree.SubElement(article, "abstract")
    abstract.text = find_paragraph(target_path, "abstract")
    
    introduction = etree.SubElement(article,"introduction")
    introduction.text = find_paragraph(target_path,"introduction")
    
    corps = etree.SubElement(article,"corps")
    corps.text = find_corps(target_path)
    
    discu = etree.SubElement(article, "Discussion")
    discu.text = find_discussion(target_path, "Discussion")
    
    conclusion = etree.SubElement(article, "conclusion")
    conclusion.text = find_paragraph(target_path, "Conclusion")
    
    biblio = etree.SubElement(article, "biblio")
    biblio.text = find_reference(target_path, "References")
    
    
    
    xmlstr = ET.tostring(article).decode('utf8')
    newxml = md.parseString(xmlstr)
    with open(output_path, "a") as output:
        output.write(newxml.toprettyxml(indent='\t',newl='\n'))





def parser_file_to_txt(filepath, output_path) :
    writer = ""
    file_name = os.path.basename(filepath).replace(".txt", ".pdf")
    title = ""
    abstract = ""
    #   -- nom de fichier --

    f = open(output_path, "a")
    f.write("le nom de ce fichier est : " + file_name + "\n")
    f.close()

    f = open(filepath, "r")
    for i in range(2) :
        title = title + f.readline().strip('\n').strip() + " "
    
    for line in f :
       if(line.lower().find("abstract") != -1):         
          break;
       writer = writer + line.strip('\n').strip()
        	
    f.close()

	
    #   -- le titre de fichier --

    f = open(output_path, "a")
    f.write("\n\n le titre de ce fichier est  : " + title.rstrip() + "\n")
    f.close()
    f = open(output_path, "a")
    f.write("\n\n les auteurs  : " + writer.rstrip() + "\n")
    f.close()

    #   -- abstract --

    abstract = find_paragraph(filepath, "abstract")
    f = open(output_path, "a")
    f.write("\n\n abstract : " + abstract)
    f.close()
    
    introduction = find_paragraph(filepath, "introduction")
    f = open(output_path, "a")
    f.write("\n\n introduction : " + introduction)
    f.close()
    
    corps = find_corps(filepath)
    f = open(output_path, "a")
    f.write("\n\n corps : " + corps)
    f.close()
    
    
    discussion = find_discussion(filepath, "Discussion")
    f = open(output_path, "a")
    f.write("\n\n discussion : " + discussion)
    f.close()
    
    
    
    conclusion = find_paragraph(filepath, "Conclusion")
    f = open(output_path, "a")
    f.write("\n\n conclusion : " + conclusion)
    f.close()
    
    
    reference = find_reference(filepath, "References")
    f = open(output_path, "a")
    f.write("\n\n references : " + reference)
    f.close()
    
    

def main():


    args = sys.argv
    filepath = args[2]   # on prends l'argument apres la commande python3 (chemin de dossier) si le code est dans le meme dossier des fichier il suffit just de mettre le nom de dossier  
    choix_option = args[1]
                  
    dossier_txt = "TEXT"
    dossier_output = create_directory("OUTPUT")
    
    files = find_ext(filepath,"pdf")
    
    pdf_to_txt(filepath)
    
    if(choix_option == "-t"): # extraire les information dans un fichier txt
    	
    	for file in files :
		
            File_txt_path = dossier_txt + "/" + os.path.basename(file).replace(".pdf", ".txt")
            output_path = dossier_output + "/" + os.path.basename(file).replace(".pdf", ".txt") 
            parser_file_to_txt(File_txt_path, output_path)

    if(choix_option == "-x"): # extraire les information dans un fichier xml
    	for file in files :
            
            File_txt_path = dossier_txt  + "/" + os.path.basename(file).replace(".pdf", ".txt")
            
            output_path =  dossier_output + "/" + os.path.basename(file).replace(".pdf", ".xml")
            parser_file_to_xml(File_txt_path, output_path)
            
    if( choix_option != "-t" and  choix_option != "-x"):
        print("merci de choisir un entre c'est deux drapeaux -t ou -x")
        return 0        
            
            
            

if __name__ == "__main__":
    main()
