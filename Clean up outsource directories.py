#https://stackoverflow.com/questions/3444645/merge-pdf-files
import shutil
import os
import sys
import tkinter
from tkinter import filedialog
import ctypes
from PyPDF2 import PdfMerger
#import logging

root = tkinter.Tk()
root.withdraw

#https://stackoverflow.com/questions/2963263/how-can-i-create-a-simple-message-box-in-python
ctypes.windll.user32.MessageBoxW(0, "Select the directory to clean.\r" + #prompt
                                 "This should be the destination directory in the outsourcing function in BidU.\r" +
                                 "This only works if you outsourced with the Tree View Folders option.",
                                 "Select folder to clean", #title
                                 0) #0=OK only

root = filedialog.askdirectory()
if root == '':
    ctypes.windll.user32.MessageBoxW(0, "Cancelled", #prompt
                                 "Finished", #title
                                 0) #0=OK only
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
    bAddedFile = False
    for folderName, subfolders, filenames in os.walk(folder):
        for filename in filenames:
            #print('found this file ' + filename)
            if os.path.splitext(filename)[1].lower() == '.pdf'.lower():
                mergefile.append(os.path.join(folder, filename))
                bAddedFile = True
                #print('adding ' +  os.path.join(folder, filename))
    newpath = os.path.join(folder, 'REDLINES')
    if not os.path.exists( newpath ):
        os.makedirs(newpath)
    #print('writing pdf to ' + os.path.join(newpath, 'REDLINES.pdf'))
    if bAddedFile:
        mergefile.write(os.path.join(newpath, 'REDLINES.pdf'))



for folderName, subfolders, filenames in os.walk(root):
    #print('Folder: ' + folderName)
    for subfolder in subfolders:
        #print('-->' + folderName + '/' + subfolder)
        moveandclean(root, root + '/' + subfolder, root + '/' + subfolder)
        
for folderName, subfolders, filenames in os.walk(root):
    for subfolder in subfolders:
        if os.path.isdir(os.path.join(root,subfolder)): #single level only
            #print('--pdfs for ' + os.path.join(root,subfolder))
            createRedlinePackage(os.path.join(root, subfolder))

            
ctypes.windll.user32.MessageBoxW(0, "Completed successfully", #prompt
                                 "Finished", #title
                                 0) #0=OK only
