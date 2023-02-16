#https://stackoverflow.com/questions/3444645/merge-pdf-files
import shutil
import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import ctypes
from PyPDF2 import PdfMerger
#import logging

#root = tkinter.Tk()
#root.withdraw


#logging.debug(root)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.prefixesCreateFolder = ['S', 's', '7', 'M', 'm']

        def moveandclean(root, moveto, folder):
            for folderName, subfolders, filenames in os.walk(folder):
                for subfolder in subfolders:
                    if subfolder[0] in self.prefixesCreateFolder:
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

            
        mainWindowSize='400x100'
        self.title('Clean and compile outsourced folders')
        self.geometry(mainWindowSize)
        self.grid()
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.frame=tk.Frame()
        self.frame.pack(expand=True)

        #label_flatten=ttk.Label(self.frame, text = 'Flatten outsourced folders created with the treeview option')
        #label_flatten.grid(row=1, column=0, sticky="w")
        
        #label_compile=ttk.Label(self.frame, 'Compile pdfs into REDLINE package')
        #label_compile.grid(row=2, grid=0, sticky="w")
        
        var_flatten = tk.IntVar()
        var_flatten.set(1)
        var_compile = tk.IntVar()
        var_compile.set(1)

        check_flatten = tk.Checkbutton(self.frame, text='Flatten outsourced folders created with the treeview option', 
            variable=var_flatten, onvalue=1, offvalue=0)
        check_flatten.grid(row=1, column=0, sticky="w", columnspan=2)
        check_compile = tk.Checkbutton(self.frame, text='Compile pdfs into REDLINE package',
            variable=var_compile, onvalue=1, offvalue=0)
        check_compile.grid(row=2, column=0, sticky="w", columnspan=2)

        def cancel_click():
            self.destroy()
            sys.exit(0)

        def ok_click():
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
            
            if var_flatten.get()==1:
                print('Flattening')
                for folderName, subfolders, filenames in os.walk(root):
                    #print('Folder: ' + folderName)
                    for subfolder in subfolders:
                        #print('-->' + folderName + '/' + subfolder)
                        moveandclean(root, root + '/' + subfolder, root + '/' + subfolder)
            if var_compile.get()==1:   
                print('Compiling')
                for folderName, subfolders, filenames in os.walk(root):
                    for subfolder in subfolders:
                        if os.path.isdir(os.path.join(root,subfolder)): #single level only
                            #print('--pdfs for ' + os.path.join(root,subfolder))
                            createRedlinePackage(os.path.join(root, subfolder))
            ctypes.windll.user32.MessageBoxW(0, "Completed successfully", #prompt
                                            "Finished", #title
                                            0) #0=OK only
                                            
            self.destroy()
            sys.exit(0)
            

        btnOK = ttk.Button(self.frame, text="Run", command=ok_click)
        btnOK.grid(row=3, column=0, sticky="nsew")

        btnCancel = ttk.Button(self.frame, text="Cancel", command=cancel_click)
        btnCancel.grid(row=3, column=1, sticky="nsew")
        

if __name__ == "__main__":
    app = App()
    app.mainloop()