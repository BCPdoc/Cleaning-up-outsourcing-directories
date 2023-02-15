#https://stackoverflow.com/questions/3444645/merge-pdf-files
import shutil
import os
import sys
import tkinter
from tkinter import filedialog
from PyPDF2 import PdfMerger
#import logging

root = tkinter.Tk()
root.withdraw

root = filedialog.askdirectory()
if root == '':
    sys.exit(0)

prefixesCreateFolder = ['S', 's', '7', 'M', 'm']

#logging.debug(root)

def moveandclean(root, moveto, folder):
    for folderName, subfolders, filenames in os.walk(folder):
        for subfolder in subfolders:
            if subfolder[0] in prefixesCreateFolder:
                newpath = root + '/' + subfolder
                if not os.path.exists( newpath ):
                    os.makedirs(newpath)
                moveandclean(root, newpath, folderName + '/' + subfolder)
            else :
                moveandclean(root, moveto,  folderName + '/' + subfolder)
        
        for file in filenames:
            if moveto != folder :
                if os.path.isfile(moveto + '/' + file):
                    os.remove(folder + '/' + file)
                else:
                    shutil.move(folder + '/' + file, moveto)
        contents = os.listdir(folder)
        if len(contents) == 0:
            os.rmdir(folder)

def createRedlinePackage(folder):
    mergefile = PdfMerger()
    for folderName, subfolders, filenames in os.walk(folder):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.pdf':
                mergefile.append(os.path.join(folder, filename))
    newpath = os.path.join(folder, 'REDLINES')
    if not os.path.exists( newpath ):
        os.makedirs(newpath)
    mergefile.write(os.path.join(newpath, 'REDLINES.pdf'))


for folderName, subfolders, filenames in os.walk(root):
    #print('Folder: ' + folderName)
    for subfolder in subfolders:
        #print('-->' + folderName + '/' + subfolder)
        moveandclean(root, root + '/' + subfolder, root + '/' + subfolder)
        
for folderName, subfolders, filenames in os.walk(root):
    for subfolder in subfolders:
        if os.path.isdir(os.path.join(root,subfolder)): #single level only
            createRedlinePackage(os.path.join(root, subfolder))