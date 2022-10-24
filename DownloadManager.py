import os
import shutil
import shelve
import time
import PySimpleGUI as pg

files = []
window = None
afm = "False"

############################################################Setup the GUI

pg.theme("DarkBlue")

layoutMain = [
    [pg.Text("Python Download Manager v1.0")],
    [pg.Text("")],
    [pg.Button("delete old files", size=(20, 2)), pg.Button("move files", size=(20, 2)), pg.Button("activate auto-file-mover", size=(20, 2)), pg.Button("exit", size=(20, 2))]
]

layoutMain_ = [
    [pg.Text("Python Download Manager v1.0")],
    [pg.Text("")],
    [pg.Button("delete old files", size=(20, 2)), pg.Button("move files", size=(20, 2)), pg.Button("activate auto-file-mover", size=(20, 2)), pg.Button("exit", size=(20, 2))]
]

layoutamfActivated = [
    [pg.Text("Python Download Manager v1.0")],
    [pg.Text("")],
    [pg.Button("delete old files", size=(25, 2)), pg.Button("deactivate auto-file-mover", size=(25, 2)), pg.Button("exit", size=(25, 2))]
]

layoutDownloadPath = [
    [pg.Text("Enter the directory of your Downloads folder if you ever manually changed it:", size=(40, 2))],
    [pg.InputText()],
    [pg.Button("next", size=(30, 1))]
]

layoutCreate = [
    [pg.Text("Enter the directory of your Downloads folder if you ever manually changed it:", size=(40, 2))],
    [pg.InputText()],
    [pg.Text("")],
    [pg.Text("Enter the directory of the Managed Downloads folder or leave it blank to keep the default path(C:/):", size=(40, 2))],
    [pg.InputText()],
    [pg.Button("generate folder", size=(30, 1))]
]

############################################################Setup file handler

# a dictionary with all file types and their corresponding directory
dirdict = {
    "" : "/DwFolder",
    ".zip" : "/DwFolder",
    ".pdf" : "/DwImages",
    ".png" : "/DwImages",
    ".jpg" : "/DwImages",
    ".exe" : "/DwExecutable",
    ".py" : "/DwExecutable",
    ".bat" : "/DwExecutable",
    ".yaml" : "/DwExecutable",
    ".jar" : "/DwExecutable",
    ".java" : "/DwExecutable",
    ".c" : "/DwExecutable",
    ".cgi" : "/DwExecutable",
    ".pl" : "/DwExecutable",
    ".class" : "/DwExecutable",
    ".ccp" : "/DwExecutable",
    ".cs" : "/DwExecutable",
    ".php" : "/DwExecutable",
    ".apk" : "/DwExecutable",
    ".bin" : "/DwExecutable",
    ".com" : "/DwExecutable",
    ".gadget" : "/DwExecutable",
    ".msi" : "/DwExecutable",
    ".wsf" : "/DwExecutable",
    ".h" : "/DwExecutable",
    ".sh" : "/DwExecutable",
    ".swift" : "/DwExecutable",
    ".vbs" : "/DwExecutable",
    ".txt" : "/DwText",
    ".tex" : "/DwText",
    ".mp3" : "/DwSound",
    ".aif" : "/DWSound",
    ".cda" : "/DwSound",
    ".mid" : "/DwSound",
    ".midi" : "/DwSound",
    ".mpa" : "/DwSound",
    ".ogg" : "/DwSound",
    ".wav" : "/DwSound",
    ".wma" : "/DwSound",
    ".wpl" : "/DwSound",
    ".xlsx" : "/DwOffice",
    ".xlx" : "/DwOffice",
    ".pptx" : "/DwOffice",
    ".ppt" : "/DwOffice",
    ".doc" : "/DwOffice",
    ".rtf" : "/DwOffice",
    ".acsm" : "/DweBook"
}

# main class
class FileHandlerClass:
    def __init__(self):
        self.DownloadPath = ""
        self.MkMD = True
        self.MDPath = ""
    
    def make_managed_downloads(self, InputDFdir, InputMDFdir): # create all folders the Download Manager needs (InputDFdir = The Path to your Downloads folder,
        os.chdir(os.path.dirname(__file__))                    # InputMDFdir = The directory of the Managed Downloads folder)
        s = shelve.open("DownloadManager") # saving all needed variables
        if InputDFdir != "":
            s["DownloadPath"] = InputDFdir
        else:
            user = str(os.popen("echo %username%").read())
            s["DownloadPath"] = r"C:\Users/{}/Downloads".format(user)
        if InputMDFdir != "":
            s["DownloadManagerPath"] = str("{}/ManagedDownloads".format(InputMDFdir))
        else:
            s["DownloadManagerPath"] = "C:/ManagedDownloads"
        s["FilePath"] = os.path.dirname(__file__)
        s["afm"] = "False"
        s.close()
        self.DownloadPath = str(InputDFdir)
        self.MDPath = str(InputMDFdir + "ManagedDownloads")
        os.mkdir(self.MDPath)# creating all the necessary folders
        os.mkdir(self.MDPath + "/DwText")
        os.mkdir(self.MDPath + "/DwVideo")
        os.mkdir(self.MDPath + "/DwExecutable")
        os.mkdir(self.MDPath + "/DwOther")
        os.mkdir(self.MDPath + "/DwSound")
        os.mkdir(self.MDPath + "/DwOffice")
        os.mkdir(self.MDPath + "/DwFolder")
        os.mkdir(self.MDPath + "/DwImages")
        os.mkdir(self.MDPath + "/DweBook")
        os.mkdir(self.MDPath + "/DwNew")
    
    def move_files(self):# a function to move a file to its corresponding directory
        os.chdir(os.path.dirname(__file__))
        os.chdir(self.DownloadPath)
        for fl in os.listdir(self.DownloadPath):
            self.move_file(fl)
    
    def move_file(self, FileToMove):# a function to loop through all files in the Downloads folder and move them with the move_files() function
        self.FN, self.FE = os.path.splitext(os.path.abspath(FileToMove))
        try:
            shutil.move(os.path.abspath(FileToMove), self.MDPath + dirdict[self.FE])
        except:
            if len(self.FE) > 4:
                shutil.move(os.path.abspath(FileToMove), self.MDPath + "/DwFolder")
            else:
                shutil.move(os.path.abspath(FileToMove), self.MDPath + "/DwOther")

    def delete_files(self): # a function to delete all files in the Managed Downloads folder if they are older than 7 days
        os.chdir(os.path.dirname(__file__))
        os.chdir(self.MDPath)
        for folder in os.listdir():# loop through DwImages, DwExecutables, DwText, etc.
            for file in os.listdir(os.path.abspath(folder)):# loop through the files in the directory
                self.TimeSinceDownload = (time.time() - os.path.getmtime(os.path.abspath(folder)+"/"+file)) / 86400
                if self.TimeSinceDownload > 7.0:
                    os.remove("{}/{}".format(str(os.path.realpath(folder)), str(file)))

    def activate_afm(self): # A function to activate the automatic-file-mover
        os.chdir(self.MDPath)
        os.chdir(os.path.dirname(__file__))
        os.system("OnStartup.pyw")

############################################################Main loop

FileHandler = FileHandlerClass()

try: # load all variables if they exist
    r = shelve.open("DownloadManager")
    FileHandler.DownloadPath = r["DownloadPath"]
    FileHandler.MDPath = r["DownloadManagerPath"]
    afm = r["afm"]
    r.close()
except: # set everythin up if they don't exist yet
    while True:
        window = pg.Window("Python Download Manager", layoutCreate, size=(400, 220), element_justification="c")
        event, values = window.read()
        match event:
            case "generate folder":
                FileHandler.make_managed_downloads(values[0], values[1])
                window.close()
                break

if __name__ == "__main__": # the main loop to detect user inputs in the GUI(The rest is self-explaining because it just uses the funcions of the main class)
    if afm == "True":
        window = pg.Window("Python Download Manager", layoutamfActivated, size=(800, 100), element_justification="c")
    else:
        window = pg.Window("Python Download Manager", layoutMain, size=(800, 100), element_justification="c")

    while True:
        event, values = window.read()
        match event:
            case "exit":
                window.close()
                break
            case "delete old files":
                FileHandler.delete_files()
            case "generate folder":
                FileHandler.make_managed_downloads(values[0], values[1])
                window.close()
                window = pg.Window("Python Download Manager", layoutMain, size=(800, 100), element_justification="c")
            case "move files":
                FileHandler.move_files()
            case "activate auto-file-mover":
                s = shelve.open("DownloadManager")
                s["afm"] = "True"
                s.close()
                FileHandler.activate_afm()
                window.close()
                window = pg.Window("Python Download Manager", layoutamfActivated, size=(800, 100), element_justification="c")
            case "deactivate auto-file-mover":
                s = shelve.open("DownloadManager")
                s["afm"] = "False"
                s.close()
                os.remove("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\OnStartup.pyw")
                os.remove("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\pyDM.bak")
                os.remove("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\pyDM.dat")
                os.remove("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\pyDM.dir")
                window.close()
                window = pg.Window("Python Download Manager", layoutMain_, size=(800, 100), element_justification="c")