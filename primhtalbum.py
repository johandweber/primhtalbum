#!/usr/bin/python3
# coding: utf-8


# primhtalbum (Primitive HTML album) is an interactive
# python3 script that creates a very simple web gallery.
# It does not intend to compete with any other of the many
# other webgallery programs and should rather be considered as
# a python exercise.
# Still I consider it quite useful if the aim is to distribute
# just a photo album based on an uncomplicated HTML interface.
# The script requires the presence of the standard UNIX file
# delete command "rm", the "zip" command line program as well as the
# "convert" an the "mogrify" programs from the Image Magick
# package. These programs can be easily installed from the
# package systems of all maior linux distributions (the program
# has been tested using Ubuntu 18.04) but are also available for
# other UNIX-like environments like MacOS X, Cygwin, or MSYS2.
#
# The to run the program, just enter the directory where the
# images you want to use in your album are (subdirectories are
# not considered). Then call, the script.
# This can also either by done by calling
# "python3 PATH_WHERE_YOUR_SCRTIPT_IS/primhtalbum.py"
# or by putting the script in your executable search path,
# making it executable (e.g. by "chmod +x primhtalbum") and
# just calling "primhtalbum.py".
# After that you will be interactively asked the title of the
# album and the size of the prview and the gallery pictures
# (the original images remain available).
#
#
# The script is licensed according to the rules of GPL,
# Version 2 (see LICENSE)
#
# (c) 2019 - 2021 by Johann Andreas Weber

import os
import shutil
import stat
import sys
import time
import webbrowser

def cleanauxil(auxil):
    shutil.rmtree(auxil, ignore_errors=True, onerror=None)

def savetitle(text):
    temptext=""
    for i in range (0,len(text)):
        if (text[i] in {" ", "/", "\\", "?","*", "$"}):
            temptext+="_"
        else:
            temptext+=text[i]
#        print ("temptext: "+temptext)
    return (temptext)

def createzip(auxil,title):
    os.system("mkdir "+savetitle(title))
    os.system("cp -r "+" index.htm "+ "*.[gG][iI][fF] *.[jJ][pP][gG] *.[pP][nN][gG] "+auxil+" "\
              + savetitle(title))
    print("Name of the zip file :  "+savetitle(title)+".zip")
    os.system("zip -r "+savetitle(title)+".zip "+savetitle(title))
    os.system("rm -r "+savetitle(title))

def write_stylesheets(auxil):
#
    maincssname=auxil+"/main.css"
    maincssfile=open(maincssname,"w")
    maincssfile.close()
#    
    slideshowcssname=auxil+"/slideshow.css"
    slideshowcssfile=open(slideshowcssname,"w")
    slideshowcssfile.write("body   {text-align: center;}\n")
    slideshowcssfile.write("img    {max-width: 80wv;\n")
    slideshowcssfile.write("        max-height: 80vh;}\n")
    slideshowcssfile.write("video  {max-width: 80wv;\n")
    slideshowcssfile.write("        max-height: 80vh;}\n")
    slideshowcssfile.write("table  {min-width: 40wv;\n")
    slideshowcssfile.write("        text-align: center;\n")
    slideshowcssfile.write("        margin-left: auto;\n")
    slideshowcssfile.write("        margin-right: auto;}\n")
    
    slideshowcssfile.write("tr     {min-width: 40vw;\n")
    slideshowcssfile.write("        text-align: center;}\n")

    slideshowcssfile.write("td     {min-width: 14vw;\n")
    
    slideshowcssfile.write("p      {min-width:40vw;\n")
    slideshowcssfile.write("        text-align: center;\n")
    slideshowcssfile.write("        margin-left: auto;\n")
    slideshowcssfile.write("        margin-right: auto;}\n")


    slideshowcssfile.close()

def write_single_images_htm(auxil,imfilelist, title,language):
    print ("Number of image files: "+str(len(imfilelist)))
    if (len(imfilelist) == 0):
        print("No files to process!")
        sys.exit()
    for i in range(0,len(imfilelist)):
        if imfilelist[i][-5:] == "webm":
            htmname=auxil+"/"+imfilelist[i][0:-5]+".htm"
        else:   
            htmname=auxil+"/"+imfilelist[i][0:-4]+".htm"
        htmfile=open(htmname,"w")
        print ("List entry #"+str(i))
        print ("Generate "+htmname+"...")
        htmfile.write("<!DOCTYPE html>\n")
        htmfile.write("<html>\n")
        htmfile.write("<head>\n")
        htmfile.write("<meta charset=\"utf8\">\n")
        htmfile.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"slideshow.css\">\n")
        htmfile.write("<title>"+title+" --- "+imfilelist[i]+"</title>\n")
        htmfile.write("</head>\n")
        htmfile.write("<body>\n")
        htmfile.write("<h3>"+title+"  --- "+imfilelist[i]+"</h3>\n")
        htmfile.write("<p>\n")
        htmfile.write("<a href=\"../"+imfilelist[i]+"\">\n")

        if ((imfilelist[i][-4:]).lower == ".gif"):
            htmfile.write("<img src=\""+imfilelist[i][0:-4]+"_gallery.gif\"></img>\n")
 
        if ((imfilelist[i][-4:]).lower() == ".jpg"):
            htmfile.write("<img src=\""+imfilelist[i][0:-4]+"_gallery.jpg\"></img>\n")

        if ((imfilelist[i][-4:]).lower() == ".png"):
            htmfile.write("<img src=\""+imfilelist[i][0:-4]+"_gallery.png\"></img>\n")
 
        htmfile.write("</a>\n")
        htmfile.write("</p>\n")

        htmfile.write("<p>\n")
        if (language == "en"):
            htmfile.write("Image "+str((i+1)) +" of "+str(len(imfilelist))+"\n")
        elif (language == "de"):
            htmfile.write("Bild "+str((i+1)) +" von "+str(len(imfilelist))+"\n")
        htmfile.write("</p>")

        htmfile.write("<p>\n")
        htmfile.write("<table>\n")
        htmfile.write("<tr>\n")

        # htmname_old and htmname_new are paths relative to the current image.
        # Thus the name of the auxiliary directory dooes not belong to
        # these variables (in contrast to htmname)
        if (i != 0):
            if imfilelist[i-1][-5:] == ".webm":
                htmname_old=imfilelist[i-1][0:-5]+".htm"
                htmfile.write("<td></td>\n")  
            else:   
                htmname_old=imfilelist[i-1][0:-4]+".htm"
            if (language== "en"):
                htmfile.write("<td><a href=\""+htmname_old+"\">previous image</a></td>\n")
            elif(language=="de"):
                htmfile.write("<td><a href=\""+htmname_old+"\">vorheriges Bild</a></td>\n")
                
        if (language =="en"):
            htmfile.write("<td><a href=\"../index.htm\"> overview </a></td>\n")
           
        elif (language == "de"):
            htmfile.write("<td><a href=\"../index.htm\"> zur Übersicht </a></td>\n")

        if (i !=len(imfilelist)-1):
            if imfilelist[i+1][-5:] == "webm":
                htmname_new=imfilelist[i+1][0:-5]+".htm"
            else:   
                htmname_new=imfilelist[i+1][0:-4]+".htm"

            if (language=="en"):
                htmfile.write("<td><a href=\""+htmname_new+"\">next image</a></td>\n")                
            elif(language=="de"):
                htmfile.write("<td><a href=\""+htmname_new+"\">nächstes Bild</a></td>\n")

        htmfile.write("</tr>\n")
        htmfile.write("</table>\n")
        htmfile.write("</p>\n")
        
        htmfile.write("</body>\n")    
        htmfile.write("</html>\n")
        print ("done\n")

    htmfile.close()

def write_index_htm(auxil,imfilelist, title, minheight, midheight, language):
    print("Generate index.htm...")
    indexfile=open("index.htm", "w")
    indexfile.write("<!DOCTYPE html>\n")
    indexfile.write("<html>\n")
    indexfile.write("<head>\n")
    indexfile.write("<meta charset=\"utf8\">\n")
    indexfile.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"slideshow.css\">\n")
    indexfile.write("<title>"+title+"</title>\n")
    indexfile.write("</head>\n")
    indexfile.write("<body>\n")
    indexfile.write("<h2>"+title+"</h2>\n")
    for i in range(0,len(imfilelist)):

        if ((imfilelist[i][-4:]).lower() == ".gif"):
            
            os.system("convert "+imfilelist[i]+" -auto-orient -geometry x"+\
                      str(minheight)+" "+auxil+"/"+imfilelist[i][0:-4]+"_small.gif")
            print(imfilelist[i] +" ==> "+" auxil/"+imfilelist[i][0:-4]+"_small.gif")

            os.system("convert "+imfilelist[i]+" -auto-orient -geometry x"+\
                      str(midheight)+" "+auxil+"/"+imfilelist[i][0:-4]+"_gallery.gif")
            print(imfilelist[i] +" ==> "+auxil+"/"+imfilelist[i][0:-4]+"_gallery.gif")            

            indexfile.write("<a href=\""+auxil+"/"+imfilelist[i][0:-4]+".htm\">\n")
            indexfile.write("<img src=\""+auxil+"/"+imfilelist[i][0:-4]+"_small.gif\"></img>\n")
            indexfile.write("</a>\n")

        if ((imfilelist[i][-4:]).lower() == ".jpg"):

            os.system("convert "+imfilelist[i]+" -auto-orient -quality 80% -geometry x"+\
                      str(minheight)+" "+auxil+"/"+imfilelist[i][0:-4]+"_small.jpg")
            print(imfilelist[i] +" ==> "+auxil+"/"+imfilelist[i][0:-4]+"_small.jpg")

            os.system("convert "+imfilelist[i]+" -auto-orient -quality 80% -geometry x"+\
                      str(midheight)+" "+auxil+"/"+imfilelist[i][0:-4]+"_gallery.jpg")
            print(imfilelist[i] +" ==> "+auxil+"/"+imfilelist[i][0:-4]+"_gallery.jpg")


            indexfile.write("<a href=\""+auxil+"/"+imfilelist[i][0:-4]+".htm\">\n")
            indexfile.write("<img src=\""+auxil+"/"+imfilelist[i][0:-4]+"_small.jpg\"></img>\n")
            indexfile.write("</a>\n")

        if ((imfilelist[i][-4:]).lower() == ".png"):
            
            os.system("convert "+imfilelist[i]+" -auto-orient -geometry x"+str(minheight)+" "+auxil+"/"+\
                      imfilelist[i][0:-4]+"_small.png")
            print(imfilelist[i] +" ==> "+auxil+"/"+imfilelist[i][0:-4]+"_small.png")            

            os.system("convert "+imfilelist[i]+" -auto-orient -geometry x"+str(midheight)+" "+auxil+"/"+\
                      imfilelist[i][0:-4]+"_gallery.png")
            print(imfilelist[i] +" ==> "+auxil+"/"+imfilelist[i][0:-4]+"_gallery.png")            

            indexfile.write("<a href=\""+imfilelist[i][0:-4]+".htm\">\n")
            indexfile.write("<img src=\""+auxil+"/"+imfilelist[i][0:-4]+"_small.jpg\"></img>\n")
            indexfile.write("</a>\n")
            
    indexfile.write("<br/>\n")

    if (language=="en"):
         indexfile.write("<a href=\""+savetitle(title)+".zip\">Here</a> is a  zip archive"+\
                        " of the web page with all images.")        
    elif (language=="de"):
        indexfile.write("<a href=\""+savetitle(title)+".zip\">Hier</a> ist ein zip-Archiv"+\
                        " der Webseite mit allen Bildern.") 
    indexfile.write("<hr/>\n")
    now=time.localtime()
    if (language=="en"):
        indexfile.write("<i>last modification:"+str(now[0])+"-"+str(now[1])+"-"+str(now[2])+"</i>\n")        
    elif (language=="de"):   
        indexfile.write("<i>Letzte Änderung:"+str(now[0])+"-"+str(now[1])+"-"+str(now[2])+"</i>\n")
    indexfile.write("</body>\n")
    indexfile.write("</html>")
    indexfile.close
    print("done")

# Main program

title= input("Please input title of gallery:")

#for thumbnails
minheight=eval(input("Please input height of thumbnail pictures in pixel:"))

#for clickimages
midheight=int(eval(input("Please input height of thumbnail pictures in click-gallery:")))
print()
print ("English...............................(1)")
print ("German................................(2)")
print
languagelist=["en","de"]
languagemenu=int(input("Please select language:"))
language=languagelist[languagemenu-1]                   
filelist=os.listdir()
filelist.sort()
#print (filelist)

imagelist=[]
videolist=[]

for file in filelist:
    if ((file[-4:]).lower() == ".jpg" or\
        (file[-4:]).lower() == ".png"or\
        (file[-4:]).lower() == ".gif"):
            print (file+"\n")
            imagelist.append(file)
            os.system("mogrify -auto-orient "+file)
print (str(len(imagelist))+" image files found:")

for file in filelist:
    if ((file[-4:]).lower() == ".mp4"  or\
        (file[-5:]).lower() == ".webm" or\
        (file[-4:]).lower() == ".gif"):
            print (file+"\n")
            videolist.append(file)
print (str(len(videolist))+" video files found:")

cleanauxil("auxil")
os.mkdir("auxil")
write_stylesheets("auxil")
write_single_images_htm("auxil",imagelist,title,language)
write_index_htm("auxil",imagelist,title, minheight, midheight,language)
print ("create zip package...")
createzip("auxil", title)
print("done")

webbrowser.open("index.htm")
